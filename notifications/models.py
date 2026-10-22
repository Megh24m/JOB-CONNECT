from django.db import models
from django.contrib.auth.models import User
from applications.models import Application

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('application_submitted', 'Application Submitted'),
        ('application_viewed', 'Application Viewed'),
        ('application_accepted', 'Application Accepted'),
        ('application_rejected', 'Application Rejected'),
        ('jobseeker_response', 'Job Seeker Responded'),
        ('general', 'General')
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    application = models.ForeignKey(
        Application,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='notifications'
    )

    notification_type = models.CharField(
        max_length=30,
        choices=NOTIFICATION_TYPES,
        default='general'
    )

    message = models.CharField(
        max_length=500
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_read = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.message