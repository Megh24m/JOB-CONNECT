from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Enter password"
            }
        )
    )


    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Confirm password"
            }
        )
    )


    role = forms.ChoiceField(
        choices=[
            ("jobseeker","Job Seeker"),
            ("employer","Employer"),
        ],
        label="Account Type",
        widget=forms.RadioSelect
    )


    class Meta:

        model = User

        fields = [
            "username",
            "email",
        ]