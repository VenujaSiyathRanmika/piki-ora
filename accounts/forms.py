from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from .models import Patient


class PatientRegistrationForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "First name",
        })
    )

    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Last name",
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Email address",
        })
    )

    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password",
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm password",
        })
    )

    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Phone number",
        })
    )

    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
            }
        )
    )

    address = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Address",
            "rows": 3,
        })
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        if User.objects.filter(username=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned_data

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data["email"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
        )

        Patient.objects.create(
            user=user,
            phone=self.cleaned_data["phone"],
            date_of_birth=self.cleaned_data["date_of_birth"],
            address=self.cleaned_data["address"],
        )

        return user


class PatientLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Email address",
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password",
        })
    )