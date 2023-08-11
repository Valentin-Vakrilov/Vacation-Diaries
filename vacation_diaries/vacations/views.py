from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import VacationForm
from .models import Vacation


class VacationAddView(LoginRequiredMixin, views.CreateView):
    template_name = "vacations/vacation-add.html"
    form_class = VacationForm

    def get_success_url(self):
        return reverse_lazy("index")

    # Set the creator of the vacation to the currently logged user
    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


class VacationDetailsView(LoginRequiredMixin, views.DetailView):
    template_name = "vacations/vacation-details.html"
    model = Vacation
    context_object_name = "vacation"

    # Validate if the creator of the vacation is the logged user
    # and if true in the template show edit and delete buttons
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        vacation = self.get_object()

        if vacation.user == self.request.user:
            creator = vacation.user
            context["creator"] = creator

        vacation_photos = vacation.photo_set.all()
        context["vacation_photos"] = vacation_photos
        return context


class VacationEditView(LoginRequiredMixin, views.UpdateView):
    template_name = "vacations/vacation-edit.html"
    model = Vacation
    form_class = VacationForm

    def get_success_url(self):
        return reverse_lazy("index")


class VacationDeleteView(LoginRequiredMixin, views.DeleteView):
    template_name = "vacations/vacation-delete.html"
    model = Vacation

    def get_success_url(self):
        return reverse_lazy("index")

    def form_valid(self, form):
        vacation = self.get_object()
        vacation.delete()
        return super().form_valid(form)
