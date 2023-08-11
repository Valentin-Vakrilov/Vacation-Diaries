from django.db import models
from .validators import max_file_size
from django.core.validators import MinLengthValidator
from vacation_diaries.accounts.models import AppUser
from vacation_diaries.vacations.models import Vacation


class Photo(models.Model):
    photo_main = models.ImageField(
        upload_to="images",
        blank=True,
        null=True,
        validators=(max_file_size,)
    )

    photo_second = models.ImageField(
        upload_to="images",
        blank=True,
        null=True,
        validators=(max_file_size,)
    )

    photo_third = models.ImageField(
        upload_to="images",
        blank=True,
        null=True,
        validators=(max_file_size,)
    )

    description = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    upload_date_and_time = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(to=AppUser, on_delete=models.CASCADE, related_name="uploaded_photos")

    vacation = models.ForeignKey(to=Vacation, on_delete=models.CASCADE)

    likes = models.ManyToManyField(AppUser, through="Like", related_name="liked_photos")

    total_likes = models.PositiveIntegerField(default=0)


class Comment(models.Model):
    COMMENT_TEXT_MAX_LENGTH = 250

    comment_text = models.TextField(
        max_length=COMMENT_TEXT_MAX_LENGTH,
        validators=(MinLengthValidator(10),),
        blank=False,
        null=False,
    )

    publication_date_and_time = models.DateTimeField(auto_now_add=True)

    commented_photo = models.ForeignKey(to=Photo, on_delete=models.CASCADE)

    user = models.ForeignKey(to=AppUser, on_delete=models.CASCADE)


class Like(models.Model):
    liked_photo = models.ForeignKey(to=Photo, on_delete=models.CASCADE)
    user = models.ForeignKey(to=AppUser, on_delete=models.CASCADE)
