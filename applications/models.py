from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job


class Application(models.Model):

    STATUS_CHOICES = (
        ('Applied', 'Applied'),
        ('Viewed', 'Viewed'),
        ('Shortlisted', 'Shortlisted'),
        ('Interview', 'Interview'),
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),
    )

    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Applied'
    )

    jobseeker_response = models.CharField(
        max_length=5,
        choices=[('yes', 'Yes, I want this job'), ('no', 'No, I am not interested')],
        blank=True,
        null=True
    )

    response_at = models.DateTimeField(blank=True, null=True)
    status_changed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"

    @property
    def waiting_days(self):
        from django.utils import timezone
        delta = timezone.now() - self.applied_at
        return delta.days


class ApplicationStatusHistory(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='history'
    )
    status = models.CharField(max_length=20)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['changed_at']

    def __str__(self):
        return f"{self.application.job.title} status to {self.status} on {self.changed_at}"