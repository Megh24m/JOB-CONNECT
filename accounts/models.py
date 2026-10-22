from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    ROLE_CHOICES = (

        ("jobseeker","Job Seeker"),

        ("employer","Employer"),

    )


    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )


    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="jobseeker"
    )


    skills = models.CharField(
        max_length=300,
        blank=True
    )


    available = models.BooleanField(
        default=True
    )

    verified = models.BooleanField(
        default=False
    )
    
    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )


    def __str__(self):

        return self.user.username


class JobSeekerSettings(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='seeker_settings'
    )
    show_datetime = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Seeker Settings"


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.content[:50]}"