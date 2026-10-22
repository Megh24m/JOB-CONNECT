from django.test import TestCase
from django.contrib.auth.models import User
from jobs.models import Job
from applications.models import Application
from reviews.models import Review
from reviews.forms import ReviewForm


class ReviewFeatureTests(TestCase):

    def setUp(self):
        # Create Employer and Job Seeker
        self.employer = User.objects.create_user(username="test_emp", password="password123")
        self.seeker1 = User.objects.create_user(username="seeker1", password="password123")
        self.seeker2 = User.objects.create_user(username="seeker2", password="password123")

        # Create Job
        self.job = Job.objects.create(
            employer=self.employer,
            title="Electrician Helper",
            company="Spark Electricals",
            location="Downtown",
            category="Electrician",
            job_type="Full Time",
            salary=25000.00,
            description="Electrician assistant post."
        )

    def test_review_allowed_only_when_selected(self):
        # seeker1 applies but is only 'Applied'
        app1 = Application.objects.create(applicant=self.seeker1, job=self.job, status="Applied")
        
        self.client.login(username="seeker1", password="password123")
        response = self.client.get(f"/reviews/add/{self.job.id}/")
        
        # Should redirect to my_applications with error message
        self.assertRedirects(response, "/applications/")
        self.assertEqual(Review.objects.count(), 0)

        # Update application status to 'Selected'
        app1.status = "Selected"
        app1.save()

        # Now GET request to review page should succeed (HTTP 200)
        response = self.client.get(f"/reviews/add/{self.job.id}/")
        self.assertEqual(response.status_code, 200)

    def test_create_and_prevent_duplicate_reviews(self):
        Application.objects.create(applicant=self.seeker1, job=self.job, status="Selected")
        self.client.login(username="seeker1", password="password123")

        # Submit first review
        post_data = {
            "rating": 5,
            "comment": "Great employer to work with!"
        }
        response = self.client.post(f"/reviews/add/{self.job.id}/", post_data)
        self.assertRedirects(response, "/applications/")
        self.assertEqual(Review.objects.count(), 1)
        
        review = Review.objects.first()
        self.assertEqual(review.reviewer, self.seeker1)
        self.assertEqual(review.employer, self.employer)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Great employer to work with!")

        # Submitting again updates existing review instead of creating duplicate
        update_data = {
            "rating": 4,
            "comment": "Updated review comment."
        }
        self.client.post(f"/reviews/add/{self.job.id}/", update_data)
        self.assertEqual(Review.objects.count(), 1)
        review.refresh_from_db()
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.comment, "Updated review comment.")

    def test_invalid_rating_and_comment(self):
        form_data_invalid_rating = {"rating": 6, "comment": "Valid comment"}
        form = ReviewForm(data=form_data_invalid_rating)
        self.assertFalse(form.is_valid())

        form_data_empty_comment = {"rating": 4, "comment": "   "}
        form = ReviewForm(data=form_data_empty_comment)
        self.assertFalse(form.is_valid())

    def test_public_visibility_rule(self):
        self.client.login(username="seeker2", password="password123")

        # Reviews section always visible — check review_count is 0 when no reviews exist
        response = self.client.get(f"/jobs/{self.job.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["review_count"], 0)
        self.assertEqual(len(response.context["employer_reviews"]), 0)

        # seeker2 cannot review without a Selected application
        self.assertFalse(response.context["can_review"])

        # After seeker1 gets Selected
        Application.objects.create(applicant=self.seeker1, job=self.job, status="Selected")

        response = self.client.get(f"/jobs/{self.job.id}/")
        self.assertEqual(response.status_code, 200)
        # seeker2 still cannot review (their application is not Selected)
        self.assertFalse(response.context["can_review"])


    def test_employer_can_review_candidate(self):
        app = Application.objects.create(applicant=self.seeker1, job=self.job, status="Selected")
        self.client.login(username="test_emp", password="password123")

        # Employer reviews the selected candidate
        post_data = {
            "rating": 5,
            "comment": "Punctual and highly skilled candidate."
        }
        response = self.client.post(f"/reviews/add/app/{app.id}/", post_data)
        self.assertRedirects(response, "/applicants/")
        
        self.assertEqual(Review.objects.count(), 1)
        review = Review.objects.first()
        self.assertEqual(review.reviewer, self.employer)
        self.assertEqual(review.reviewee, self.seeker1)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Punctual and highly skilled candidate.")


