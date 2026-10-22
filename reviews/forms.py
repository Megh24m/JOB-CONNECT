from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = [
            "rating",
            "comment"
        ]
        widgets = {
            "rating": forms.Select(attrs={
                "class": "form-select",
                "style": "width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 15px;"
            }),
            "comment": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Share your experience working with this employer...",
                "style": "width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 14px; font-family: inherit;"
            }),
        }
        labels = {
            "rating": "Rating (1 - 5 Stars)",
            "comment": "Review / Feedback"
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is None or rating < 1 or rating > 5:
            raise forms.ValidationError("Please select a valid rating between 1 and 5.")
        return rating

    def clean_comment(self):
        comment = self.cleaned_data.get('comment', '')
        if not comment or not comment.strip():
            raise forms.ValidationError("Comment cannot be empty.")
        return comment.strip()