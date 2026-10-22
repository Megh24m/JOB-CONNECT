from django.shortcuts import render, redirect
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from .models import Profile, JobSeekerSettings, Message

from jobs.models import Job, SavedJob
from applications.models import Application
from notifications.models import Notification



# ---------------- HOME ---------------- #

def home(request):

    return render(
        request,
        "home.html"
    )



# ---------------- REGISTER ---------------- #

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]

            email = form.cleaned_data["email"]


            if User.objects.filter(username=username).exists():

                messages.error(
                    request,
                    "Username already exists."
                )

                return render(
                    request,
                    "register.html",
                    {"form": form}
                )


            if User.objects.filter(email=email).exists():

                messages.error(
                    request,
                    "Email already exists."
                )

                return render(
                    request,
                    "register.html",
                    {"form": form}
                )



            user = User.objects.create_user(
                username=username,
                email=email,
                password=form.cleaned_data["password1"]
            )

            role = form.cleaned_data["role"]
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={"role": role}
            )
            if not created and profile.role != role:
                profile.role = role
                profile.save()

            if role == "jobseeker":
                JobSeekerSettings.objects.get_or_create(user=user)



            messages.success(
                request,
                "Registration Successful! Please Login."
            )


            return redirect("login")



    else:

        form = RegisterForm()



    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )





# ---------------- LOGIN ---------------- #

def login_view(request):

    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(user=request.user)
        if profile.role == "employer":
            return redirect("employer_dashboard")
        else:
            return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(
                request,
                user
            )
            messages.success(
                request,
                "Login Successful!"
            )

            profile, _ = Profile.objects.get_or_create(user=user)
            if profile.role == "employer":
                return redirect("employer_dashboard")
            else:
                return redirect("dashboard")

        else:
            messages.error(
                request,
                "Invalid Username or Password"
            )



    return render(
        request,
        "login.html"
    )





# ---------------- JOB SEEKER DASHBOARD ---------------- #

@login_required
def dashboard(request):
    application_count = Application.objects.filter(
        applicant=request.user
    ).count()

    available_jobs = Job.objects.filter(
        status="Open"
    ).count()

    saved_count = SavedJob.objects.filter(
        user=request.user
    ).count()

    notifications_count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    recent_activities = Application.objects.filter(
        applicant=request.user
    ).order_by('-applied_at')[:5]

    return render(
        request,
        "dashboard.html",
        {
            "applications": application_count,
            "jobs": available_jobs,
            "saved_count": saved_count,
            "notifications_count": notifications_count,
            "recent_activities": recent_activities,
        }
    )





# ---------------- EMPLOYER DASHBOARD ---------------- #

@login_required
def employer_dashboard(request):

    jobs = Job.objects.filter(
        employer=request.user
    )


    total_jobs = jobs.count()



    applications = Application.objects.filter(
        job__employer=request.user
    )



    total_applications = applications.count()



    hired = applications.filter(
        status="Hired"
    ).count()



    return render(

        request,

        "employer_dashboard.html",

        {
            "jobs": jobs,
            "total_jobs": total_jobs,
            "total_applications": total_applications,
            "hired": hired
        }

    )





# ---------------- APPLICANTS ---------------- #

@login_required
def applicants(request):
    from reviews.models import Review

    applications = Application.objects.filter(
        job__employer=request.user
    ).order_by("-applied_at")

    for app in applications:
        if app.status in ['Selected', 'Hired']:
            app.can_review = True
            app.employer_review = Review.objects.filter(
                reviewer=request.user,
                job=app.job,
                reviewee=app.applicant
            ).first()
        else:
            app.can_review = False

    return render(
        request,
        "applicants.html",
        {
            "applications": applications
        }
    )






# ---------------- LOGOUT ---------------- #

def logout_view(request):

    logout(request)


    messages.success(
        request,
        "Logged out successfully."
    )


    return redirect("login")

@login_required
def profile(request):
    profile_obj, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()

        if email:
            # Check email uniqueness if changed
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.error(request, "This email is already in use by another account.")
            else:
                request.user.email = email
                request.user.first_name = first_name
                request.user.last_name = last_name
                request.user.save()

                if profile_obj.role == "jobseeker":
                    skills = request.POST.get("skills", "").strip()
                    available = request.POST.get("available") == "on"
                    profile_obj.skills = skills
                    profile_obj.available = available
                    profile_obj.save()

                messages.success(request, "Profile updated successfully!")
                return redirect("profile")

    context = {
        "profile": profile_obj,
    }

    if profile_obj.role == "employer":
        jobs = Job.objects.filter(employer=request.user)
        applications = Application.objects.filter(job__employer=request.user)
        recent_jobs = jobs.order_by("-created_at")[:5]
        primary_company = recent_jobs.first().company if recent_jobs.exists() else "Not Specified"

        context.update({
            "total_jobs": jobs.count(),
            "active_jobs": jobs.filter(status="Open").count(),
            "total_applications": applications.count(),
            "hired": applications.filter(status="Hired").count(),
            "recent_jobs": recent_jobs,
            "company_name": primary_company,
        })

    return render(
        request,
        "profile.html",
        context
    )

@login_required
def employer_detail(request, employer_id):
    # Show employer profile to job seekers or other users
    employer_user = User.objects.get(id=employer_id)
    profile_obj, _ = Profile.objects.get_or_create(user=employer_user)

    # Gather employer job stats
    jobs = Job.objects.filter(employer=employer_user)
    applications = Application.objects.filter(job__employer=employer_user)
    recent_jobs = jobs.order_by('-created_at')[:5]
    company_name = recent_jobs.first().company if recent_jobs.exists() else "Not Specified"

    context = {
        "profile": profile_obj,
        "request_user": request.user,
        "total_jobs": jobs.count(),
        "active_jobs": jobs.filter(status="Open").count(),
        "total_applications": applications.count(),
        "hired": applications.filter(status="Hired").count(),
        "recent_jobs": recent_jobs,
        "company_name": company_name,
        "is_owner": request.user == employer_user,
    }
    return render(request, "profile.html", context)

@login_required
def settings_view(request):
    settings_obj, created = JobSeekerSettings.objects.get_or_create(user=request.user)
    if request.method == "POST":
        show_datetime = request.POST.get("show_datetime") == "on"
        settings_obj.show_datetime = show_datetime
        settings_obj.save()
        messages.success(request, "Settings updated successfully.")
        return redirect("settings_view")
    return render(request, "settings.html", {"settings": settings_obj})


# ---------------- MESSAGES ---------------- #

@login_required
def messages_view(request):
    current_user = request.user
    is_employer = hasattr(current_user, 'profile') and current_user.profile.role == 'employer'

    # Build contacts list from real application connections
    contacts = []
    contact_ids = set()

    if is_employer:
        # Employer sees job seekers who applied to their jobs
        apps = Application.objects.filter(
            job__employer=current_user
        ).select_related('applicant', 'job')
        for app in apps:
            if app.applicant.id not in contact_ids and app.applicant.id != current_user.id:
                contact_ids.add(app.applicant.id)
                last_msg = Message.objects.filter(
                    models.Q(sender=current_user, receiver=app.applicant) |
                    models.Q(sender=app.applicant, receiver=current_user)
                ).order_by('-created_at').first()
                unread_count = Message.objects.filter(
                    sender=app.applicant,
                    receiver=current_user,
                    is_read=False
                ).count()
                contacts.append({
                    'user': app.applicant,
                    'job_title': app.job.title,
                    'last_message': last_msg,
                    'unread_count': unread_count,
                })
    else:
        # Job seeker sees employers whose jobs they applied to
        apps = Application.objects.filter(
            applicant=current_user
        ).select_related('job')
        for app in apps:
            employer = app.job.employer
            display_user = employer
            if display_user.id not in contact_ids:
                contact_ids.add(display_user.id)
                last_msg = Message.objects.filter(
                    models.Q(sender=current_user, receiver=employer) |
                    models.Q(sender=employer, receiver=current_user)
                ).order_by('-created_at').first()
                unread_count = Message.objects.filter(
                    sender=employer,
                    receiver=current_user,
                    is_read=False
                ).count()
                contacts.append({
                    'user': display_user,
                    'job_title': app.job.title,
                    'last_message': last_msg,
                    'unread_count': unread_count,
                })

    # Include all users who have sent or received messages with current user
    sent_to = Message.objects.filter(sender=current_user).values_list('receiver', flat=True).distinct()
    rec_from = Message.objects.filter(receiver=current_user).values_list('sender', flat=True).distinct()
    all_partners = set(sent_to).union(set(rec_from))

    for partner_id in all_partners:
        if partner_id not in contact_ids and partner_id != current_user.id:
            contact_ids.add(partner_id)
            try:
                partner_user = User.objects.get(id=partner_id)
                last_msg = Message.objects.filter(
                    models.Q(sender=current_user, receiver=partner_user) |
                    models.Q(sender=partner_user, receiver=current_user)
                ).order_by('-created_at').first()
                unread_count = Message.objects.filter(
                    sender=partner_user,
                    receiver=current_user,
                    is_read=False
                ).count()
                contacts.append({
                    'user': partner_user,
                    'job_title': '',
                    'last_message': last_msg,
                    'unread_count': unread_count,
                })
            except User.DoesNotExist:
                pass

    # Sort contacts: unread first, then by last message time
    contacts.sort(
        key=lambda c: (
            -(c['unread_count']),
            -(c['last_message'].created_at.timestamp() if c['last_message'] else 0)
        )
    )

    # Determine active chat partner
    chat_with_id = request.GET.get('chat_with')
    chat_user = None
    chat_messages = []

    if chat_with_id:
        try:
            chat_user = User.objects.get(id=int(chat_with_id))
            chat_messages = Message.objects.filter(
                models.Q(sender=current_user, receiver=chat_user) |
                models.Q(sender=chat_user, receiver=current_user)
            ).order_by('created_at')

            # Mark messages from chat_user as read
            Message.objects.filter(
                sender=chat_user,
                receiver=current_user,
                is_read=False
            ).update(is_read=True)

            # Refresh unread count for this contact
            for c in contacts:
                if c['user'].id == chat_user.id:
                    c['unread_count'] = 0
                    break

        except (User.DoesNotExist, ValueError):
            chat_user = None

    elif contacts:
        # Auto-select first contact
        chat_user = contacts[0]['user']
        chat_messages = Message.objects.filter(
            models.Q(sender=current_user, receiver=chat_user) |
            models.Q(sender=chat_user, receiver=current_user)
        ).order_by('created_at')

        Message.objects.filter(
            sender=chat_user,
            receiver=current_user,
            is_read=False
        ).update(is_read=True)
        if contacts:
            contacts[0]['unread_count'] = 0

    return render(
        request,
        "messages.html",
        {
            "contacts": contacts,
            "chat_user": chat_user,
            "chat_messages": chat_messages,
            "is_employer": is_employer,
        }
    )


@login_required
def send_message(request):
    if request.method == "POST":
        receiver_id = request.POST.get("receiver_id")
        content = request.POST.get("content", "").strip()

        if receiver_id and content:
            try:
                receiver = User.objects.get(id=int(receiver_id))
                Message.objects.create(
                    sender=request.user,
                    receiver=receiver,
                    content=content
                )
                # Create notification for recipient
                Notification.objects.create(
                    user=receiver,
                    message=f"💬 New message from {request.user.username}: {content[:35]}"
                )
            except (User.DoesNotExist, ValueError):
                pass

        return redirect(f"/messages/?chat_with={receiver_id}")

    return redirect("messages")