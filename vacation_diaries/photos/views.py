from django.shortcuts import get_object_or_404, redirect
from django.views import generic as views
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import PhotoForm, PhotoCommentForm, PhotoEditForm
from vacation_diaries.vacations.models import Vacation
from .models import Photo, Comment, Like
from django.core.exceptions import ValidationError, PermissionDenied


class PhotoAddView(LoginRequiredMixin, views.CreateView):
    template_name = "photos/photo-add.html"
    form_class = PhotoForm

    def get_success_url(self):
        return reverse_lazy("index")

    def form_valid(self, form):
        form.instance.user = self.request.user

        vacation_pk = self.request.POST.get("vacation")
        vacation = get_object_or_404(Vacation, id=vacation_pk)

        vacation_photo_main = vacation.photo_set.filter(photo_main__gt=1).exists()
        vacation_photo_second = vacation.photo_set.filter(photo_second__gt=1).exists()
        vacation_photo_third = vacation.photo_set.filter(photo_third__gt=1).exists()

        if vacation.user != self.request.user:
            raise PermissionDenied("You do not have permission to add photos to this vacation.")

        if form.cleaned_data.get("photo_main") and vacation_photo_main:
            raise ValidationError("A photo is already loaded!")
        elif form.cleaned_data.get("photo_second") and vacation_photo_second:
            raise ValidationError("A photo is already loaded!")
        elif form.cleaned_data.get("photo_third") and vacation_photo_third:
            raise ValidationError("A photo is already loaded!")

        form.instance.vacation = vacation

        return super().form_valid(form)


class PhotoDetailsView(LoginRequiredMixin, views.DetailView):
    template_name = "photos/photo-details.html"
    model = Photo
    context_object_name = "photo"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        photo = self.get_object()

        comments = Comment.objects.filter(commented_photo=photo)
        comment_form = PhotoCommentForm()

        try:
            context["user_liked_photo"] = True
        except Like.DoesNotExist:
            context["user_liked_photo"] = False

        context["comments"] = comments
        context["comment_form"] = comment_form
        context["total_likes"] = photo.like_set.count()

        if photo.user == self.request.user:
            creator = photo.user
            context["creator"] = creator

        return context


class PhotoEditView(LoginRequiredMixin, views.UpdateView):
    template_name = "photos/photo-edit.html"
    model = Photo
    form_class = PhotoEditForm

    def get_success_url(self):
        vacation_pk = self.object.vacation.pk
        return reverse_lazy("vacation_details", kwargs={"pk": vacation_pk})


class PhotoDeleteView(LoginRequiredMixin, views.DeleteView):
    template_name = "photos/photo-delete.html"
    model = Photo

    def get_success_url(self):
        vacation_pk = self.object.vacation.pk
        return reverse_lazy("vacation_details", kwargs={"pk": vacation_pk})

    def form_valid(self, form):
        photo = self.get_object()
        photo.delete()
        return super().form_valid(form)


class PhotoCommentAddView(LoginRequiredMixin, views.CreateView):
    template_name = "photos/photo-comment-add.html"
    form_class = PhotoCommentForm
    model = Comment

    def get_success_url(self):
        return reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["photo_pk"] = self.kwargs["pk"]
        return context

    def form_valid(self, form):
        photo_pk = self.kwargs["pk"]
        photo = get_object_or_404(Photo, pk=photo_pk)
        form.instance.commented_photo = photo
        form.instance.user = self.request.user

        return super().form_valid(form)


class PhotoCommentEditView(LoginRequiredMixin, views.UpdateView):
    template_name = "photos/photo-comment-edit.html"
    model = Comment
    form_class = PhotoCommentForm

    def get_success_url(self):
        return reverse_lazy("index")


class PhotoCommentDeleteView(LoginRequiredMixin, views.DeleteView):
    template_name = "photos/photo-comment-delete.html"
    model = Comment

    def get_success_url(self):
        return reverse_lazy("index")

    def form_valid(self, form):
        comment = self.get_object()
        comment.delete()
        return super().form_valid(form)


class LikePhotoToggleView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        photo = get_object_or_404(Photo, pk=kwargs["pk"])
        user = self.request.user

        try:
            liked_photo = Like.objects.get(user=user, liked_photo=photo)
            liked_photo.delete()
            photo.total_likes -= 1
            photo.save()
        except Like.DoesNotExist:
            Like.objects.create(user=user, liked_photo=photo)
            photo.total_likes += 1
            photo.save()

        return redirect("index")
