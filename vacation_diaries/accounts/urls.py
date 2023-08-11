from django.urls import path
from vacation_diaries.accounts.views import RegisterUserView, LoginUserView, LogoutUserView, ProfileDetailsView, \
    ProfileEditView, ProfileDeleteView, ChangePasswordView

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("profile/<int:pk>/", ProfileDetailsView.as_view(), name="profile_details"),
    path("profile/<int:pk>/edit/", ProfileEditView.as_view(), name="profile_edit"),
    path("profile/<int:pk>/delete/", ProfileDeleteView.as_view(), name="profile_delete")
]
