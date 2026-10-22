from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from jobs.models import Job


class Review(models.Model):

    RATING_CHOICES = (
        (1, "⭐"),
        (2, "⭐⭐"),
        (3, "⭐⭐⭐"),
        (4, "⭐⭐⭐⭐"),
        (5, "⭐⭐⭐⭐⭐"),
    )

    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="given_reviews"
    )

    reviewee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_reviews",
        null=True,
        blank=True
    )

    employer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="employer_reviews"
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('reviewer', 'job', 'reviewee')
        ordering = ['-created_at']

    def __str__(self):
        target = self.reviewee.username if self.reviewee else self.employer.username
        return f"{self.reviewer.username} -> {target} ({self.rating}⭐)"
