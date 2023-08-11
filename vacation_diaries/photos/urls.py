from django.urls import path, include
from .views import PhotoAddView, PhotoDetailsView, PhotoEditView, PhotoDeleteView, PhotoCommentAddView, \
    PhotoCommentEditView, PhotoCommentDeleteView, LikePhotoToggleView

urlpatterns = [
    path("add/", PhotoAddView.as_view(), name="photo_add"),
    path("photo/<int:pk>/", include([
        path("", PhotoDetailsView.as_view(), name="photo_details"),
        path("edit/", PhotoEditView.as_view(), name="photo_edit"),
        path("delete/", PhotoDeleteView.as_view(), name="photo_delete"),
        path("like/", LikePhotoToggleView.as_view(), name="photo_like_toggle")
    ])),
    path("photo/<int:pk>/comment/", include([
        path("add/", PhotoCommentAddView.as_view(), name="photo_comment_add"),
        path("edit/", PhotoCommentEditView.as_view(), name="photo_comment_edit"),
        path("delete/", PhotoCommentDeleteView.as_view(), name="photo_comment_delete"),
    ])),
]
