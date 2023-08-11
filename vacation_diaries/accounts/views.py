from django.contrib.auth import login, views as auth_views
from django.urls import reverse_lazy
from django.views import generic as views
from vacation_diaries.accounts.forms import RegisterUserForm, ProfileEditForm, ChangePasswordForm
from .models import Profile
from django.templatetags.static import static
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView


class RegisterUserView(views.CreateView):
    template_name = "accounts/register.html"
    form_class = RegisterUserForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        result = super().form_valid(form)

        login(self.request, self.object)

        return result


class LoginUserView(auth_views.LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self):
        return reverse_lazy("index")


class LogoutUserView(auth_views.LogoutView):
    pass


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = "accounts/change-password.html"
    form_class = ChangePasswordForm

    def get_success_url(self):
        return reverse_lazy("profile_details", kwargs={"pk": self.request.user.pk})


class ProfileDetailsView(LoginRequiredMixin, views.DetailView):
    template_name = "accounts/profile-details.html"
    model = Profile
    profile_picture = static("app_images/no_profile_image.png")

    def set_profile_picture(self):
        if self.object.image is not None:
            return self.object.image
        return self.profile_picture


class ProfileEditView(LoginRequiredMixin, views.UpdateView):
    template_name = "accounts/profile-edit.html"
    model = Profile
    form_class = ProfileEditForm

    def get_success_url(self):
        return reverse_lazy("profile_details", kwargs={"pk": self.object.pk})


class ProfileDeleteView(LoginRequiredMixin, views.DeleteView):
    template_name = "accounts/profile-delete.html"
    model = Profile

    def get_success_url(self):
        return reverse_lazy("index")

    def form_valid(self, form):
        profile = self.get_object()
        user = profile.user
        user.delete()
        profile.delete()
        return super().form_valid(form)
