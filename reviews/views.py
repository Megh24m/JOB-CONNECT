from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Review
from .forms import ReviewForm
from jobs.models import Job
from applications.models import Application


@login_required
def add_review_app(request, app_id):
    application = get_object_or_404(Application, id=app_id)
    job = application.job

    is_applicant = (request.user == application.applicant)
    is_employer = (request.user == job.employer)

    if not (is_applicant or is_employer):
        messages.error(request, "You are not authorized to review this application.")
        return redirect("my_applications" if is_applicant else "applicants")

    if application.status not in ['Selected', 'Hired']:
        messages.error(request, "Reviews can only be submitted after application reaches Selected or Hired status.")
        if is_employer:
            return redirect("applicants")
        return redirect("my_applications")

    if is_applicant:
        reviewee = job.employer
        target_name = f"Employer ({job.company})"
        redirect_url = "my_applications"
    else:
        reviewee = application.applicant
        target_name = f"Candidate ({application.applicant.username})"
        redirect_url = "applicants"

    existing_review = Review.objects.filter(
        reviewer=request.user,
        job=job,
        reviewee=reviewee
    ).first()

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewee = reviewee
            review.employer = job.employer
            review.job = job
            review.save()

            messages.success(request, f"Your review for {target_name} has been saved successfully.")
            return redirect(redirect_url)
    else:
        form = ReviewForm(instance=existing_review)

    return render(
        request,
        "reviews.html",
        {
            "form": form,
            "job": job,
            "application": application,
            "target_name": target_name,
            "existing_review": existing_review
        }
    )


@login_required
def add_review(request, id):
    application = Application.objects.filter(
        applicant=request.user,
        job_id=id,
        status__in=['Selected', 'Hired']
    ).first()

    if not application:
        application = Application.objects.filter(
            job__employer=request.user,
            job_id=id,
            status__in=['Selected', 'Hired']
        ).first()

    if not application:
        messages.error(request, "You can only review after an application reaches Selected or Hired status.")
        return redirect("my_applications")

    return add_review_app(request, application.id)
