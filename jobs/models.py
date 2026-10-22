from django.db import models
from django.contrib.auth.models import User


# ==========================
# JOB MODEL
# ==========================

class Job(models.Model):

    CATEGORY_CHOICES = (
        ('Retail Shop', 'Retail Shop'),
        ('Supermarket', 'Supermarket'),
        ('Hotel', 'Hotel'),
        ('Restaurant', 'Restaurant'),
        ('Bakery', 'Bakery'),
        ('Delivery', 'Delivery'),
        ('Driver', 'Driver'),
        ('Electrician', 'Electrician'),
        ('Plumber', 'Plumber'),
        ('Tailor', 'Tailor'),
        ('House Maid', 'House Maid'),
        ('Cook', 'Cook'),
        ('Helper', 'Helper'),
        ('Security', 'Security'),
        ('Cleaning', 'Cleaning'),
        ('Receptionist', 'Receptionist'),
        ('Other', 'Other'),
    )

    JOB_TYPE_CHOICES = (
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Temporary', 'Temporary'),
        ('Contract', 'Contract'),
        ('Daily Wage', 'Daily Wage'),
        ('Internship', 'Internship'),
    )

    employer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=150)

    company = models.CharField(max_length=150)

    location = models.CharField(max_length=100)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES,
        default='Full Time'
    )

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField()

    vacancy = models.PositiveIntegerField(default=1)

    status = models.CharField(
        max_length=20,
        default="Open"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ==========================
# SAVE JOB FEATURE ❤️
# ==========================

class SavedJob(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    saved_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username + " saved " + self.job.title


# ==========================
# RECENTLY VIEWED JOB FEATURE 👁
# ==========================

class RecentlyViewed(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    viewed_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username + " viewed " + self.job.title