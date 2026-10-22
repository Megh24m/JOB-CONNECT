from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone


from .models import Job, SavedJob, RecentlyViewed
from .forms import JobForm
from applications.models import Application
from reviews.models import Review
from django.db.models import Avg






# ---------------- JOB LIST ---------------- #

@login_required
def job_list(request):

    jobs = Job.objects.filter(
        status="Open"
    ).order_by("-created_at")


    search = request.GET.get("search")

    location = request.GET.get("location")

    category = request.GET.get("category")

    job_type = request.GET.get("job_type")

    if search:

        jobs = jobs.filter(
            Q(title__icontains=search) |
            Q(company__icontains=search)
        )


    if location:

        jobs = jobs.filter(
            location__icontains=location
        )


    if category:
        jobs = jobs.filter(
            category=category
        )

    if job_type:
        jobs = jobs.filter(
            job_type=job_type
        )


    return render(
        request,
        "job_list.html",
        {
            "jobs": jobs
        }
    )






# ---------------- CREATE JOB ---------------- #

@login_required
def create_job(request):

    if request.method == "POST":

        form = JobForm(request.POST)


        if form.is_valid():

            job = form.save(commit=False)

            job.employer = request.user

            job.save()


            return redirect(
                "job_list"
            )


    else:

        form = JobForm()



    return render(
        request,
        "create_job.html",
        {
            "form": form
        }
    )






# ---------------- JOB DETAIL ---------------- #

@login_required
def job_detail(request, id):
    job = get_object_or_404(Job, id=id)

    already_applied = Application.objects.filter(
        applicant=request.user,
        job=job
    ).exists()

    already_saved = SavedJob.objects.filter(
        user=request.user,
        job=job
    ).exists()

    recent = RecentlyViewed.objects.filter(
        user=request.user,
        job=job
    ).first()

    if recent:
        RecentlyViewed.objects.filter(id=recent.id).update(viewed_at=timezone.now())
    else:
        RecentlyViewed.objects.create(
            user=request.user,
            job=job
        )

    # Always load employer reviews (section always visible like shopping apps)
    employer_reviews = Review.objects.filter(
        employer=job.employer,
        reviewee=job.employer  # job seekers review the employer (reviewee = employer)
    ).order_by("-created_at")
    review_count = employer_reviews.count()
    avg_rating = 0
    rating_distribution = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}

    if review_count > 0:
        avg = employer_reviews.aggregate(Avg("rating"))["rating__avg"]
        avg_rating = round(avg, 1) if avg else 0
        for r in employer_reviews:
            key = r.rating
            if key in rating_distribution:
                rating_distribution[key] += 1

    # Can this user review this specific job's employer?
    can_review = Application.objects.filter(
        applicant=request.user,
        job=job,
        status__in=['Selected', 'Hired']
    ).exists()

    existing_user_review = None
    if can_review:
        existing_user_review = Review.objects.filter(
            reviewer=request.user,
            job=job,
            reviewee=job.employer
        ).first()

    return render(
        request,
        "job_detail.html",
        {
            "job": job,
            "already_applied": already_applied,
            "already_saved": already_saved,
            "employer_reviews": employer_reviews,
            "avg_rating": avg_rating,
            "review_count": review_count,
            "rating_distribution": rating_distribution,
            "can_review": can_review,
            "existing_user_review": existing_user_review,
        }
    )






# ---------------- SAVE JOB ---------------- #

@login_required
def save_job(request,id):

    job = get_object_or_404(
        Job,
        id=id
    )


    saved = SavedJob.objects.filter(
        user=request.user,
        job=job
    ).exists()



    if not saved:

        SavedJob.objects.create(
            user=request.user,
            job=job
        )


    return redirect(
        "saved_jobs"
    )






# ---------------- SAVED JOBS ---------------- #

@login_required
def saved_jobs(request):

    jobs = SavedJob.objects.filter(
        user=request.user
    ).order_by(
        "-saved_at"
    )


    return render(
        request,
        "saved_jobs.html",
        {
            "jobs":jobs
        }
    )







# ---------------- RECENTLY VIEWED ---------------- #

@login_required
def recently_viewed(request):

    recent_records = RecentlyViewed.objects.filter(
        user=request.user
    ).order_by(
        "-viewed_at"
    )

    seen_jobs = set()
    unique_jobs = []
    for rv in recent_records:
        if rv.job_id not in seen_jobs:
            seen_jobs.add(rv.job_id)
            unique_jobs.append(rv)
            if len(unique_jobs) == 10:
                break

    return render(
        request,
        "recently_viewed.html",
        {
            "jobs": unique_jobs
        }
    )







# ---------------- SEARCH SUGGESTIONS ---------------- #

def search_suggestions(request):

    query = request.GET.get("q", "")

    jobs = Job.objects.filter(
    Q(title__icontains=query) |
    Q(company__icontains=query)
     )[:5]


    data = []


    for job in jobs:

        data.append(
            job.title
        )


    return JsonResponse(
        data,
        safe=False
    )