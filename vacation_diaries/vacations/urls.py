from django.urls import path, include
from .views import VacationAddView, VacationDetailsView, VacationEditView, VacationDeleteView

urlpatterns = [
    path("add/", VacationAddView.as_view(), name="vacation_add"),
    path("vacation/<int:pk>/", include([
        path("", VacationDetailsView.as_view(), name="vacation_details"),
        path("edit/", VacationEditView.as_view(), name="vacation_edit"),
        path("delete/", VacationDeleteView.as_view(), name="vacation_delete")
    ]))
]
