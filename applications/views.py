from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Application, ApplicationStatusHistory
from jobs.models import Job
from notifications.models import Notification
from reviews.models import Review


@login_required
def apply_job(request, id):
    job = get_object_or_404(Job, id=id)
    already_applied = Application.objects.filter(
        applicant=request.user,
        job=job
    ).exists()

    if not already_applied:
        app = Application.objects.create(
            applicant=request.user,
            job=job,
            status="Applied",
            status_changed_at=timezone.now()
        )
        
        # Add to status history
        ApplicationStatusHistory.objects.create(
            application=app,
            status="Applied"
        )

        # Notify Job Seeker
        Notification.objects.create(
            user=request.user,
            application=app,
            notification_type='application_submitted',
            message=f"You successfully applied for {job.title} at {job.company}."
        )

    return redirect("my_applications")


@login_required
def my_applications(request):
    applications = Application.objects.filter(
        applicant=request.user
    ).order_by("-applied_at")

    # Attach review info to selected/hired applications
    for app in applications:
        if app.status in ['Selected', 'Hired']:
            app.review = Review.objects.filter(
                reviewer=request.user,
                job=app.job,
                reviewee=app.job.employer
            ).first()
            app.can_review = True
        else:
            app.review = None
            app.can_review = False

    # Fetch settings to check date/time display
    show_datetime = True
    if hasattr(request.user, 'seeker_settings'):
        show_datetime = request.user.seeker_settings.show_datetime

    return render(
        request,
        "my_applications.html",
        {
            "applications": applications,
            "show_datetime": show_datetime,
        }
    )



@login_required
def update_application_status(request, id, status):
    application = get_object_or_404(Application, id=id)

    # Allow employer to update status
    if application.job.employer == request.user:
        application.status = status
        application.status_changed_at = timezone.now()
        application.save()

        # Add to status history
        ApplicationStatusHistory.objects.create(
            application=application,
            status=status
        )

        # Determine notification details
        notif_type = 'general'
        msg = f"Your application status for {application.job.title} has been updated to {status}."

        if status == 'Viewed':
            notif_type = 'application_viewed'
            msg = f"Your application for {application.job.title} has been viewed by the employer."
        elif status in ['Selected', 'Hired', 'Interview', 'Shortlisted']:
            notif_type = 'application_accepted'
            msg = f"Your application for {application.job.title} has been accepted by the employer."
        elif status == 'Rejected':
            notif_type = 'application_rejected'
            msg = f"Your application for {application.job.title} has been rejected."

        # Create Seeker notification
        Notification.objects.create(
            user=application.applicant,
            application=application,
            notification_type=notif_type,
            message=msg
        )

    return redirect("employer_dashboard")


@login_required
def respond_to_offer(request, id, response):
    application = get_object_or_404(Application, id=id, applicant=request.user)

    if response in ['yes', 'no']:
        application.jobseeker_response = response
        application.response_at = timezone.now()
        application.save()

        # Notify the employer
        choice_str = "Accepted" if response == 'yes' else "Declined"
        msg = f"Candidate {request.user.username} has {choice_str} your job offer for {application.job.title}."
        
        Notification.objects.create(
            user=application.job.employer,
            application=application,
            notification_type='jobseeker_response',
            message=msg
        )

    return redirect("my_applications")