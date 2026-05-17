from django import forms
from django.contrib.auth.hashers import make_password

from .models import EventRegistration


class EventRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = EventRegistration
        fields = ["full_name", "email", "age", "password"]

    def clean_full_name(self):
        full_name = self.cleaned_data["full_name"].strip()
        if len(full_name) < 5:
            raise forms.ValidationError("Full name must be at least 5 characters.")
        return full_name

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if not email.endswith("@gmail.com"):
            raise forms.ValidationError("Email must end with @gmail.com.")
        return email

    def clean_age(self):
        age = self.cleaned_data["age"]
        if age < 18:
            raise forms.ValidationError("Age must be 18 and above.")
        return age

    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters.")
        return password

    def save(self, commit=True):
        registration = super().save(commit=False)
        registration.password = make_password(self.cleaned_data["password"])
        if commit:
            registration.save()
        return registration
