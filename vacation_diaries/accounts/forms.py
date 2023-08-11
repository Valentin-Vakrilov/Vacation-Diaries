from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import PasswordChangeForm
from vacation_diaries.accounts.models import AppUser, Profile
from django import forms


class RegisterUserForm(auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = AppUser
        fields = ("username", "email", "password1", "password2",)


class ChangePasswordForm(PasswordChangeForm):
    pass


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]
