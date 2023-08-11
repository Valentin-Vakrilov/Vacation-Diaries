from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from vacation_diaries.accounts.models import AppUser


class Vacation(models.Model):
    destination = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        validators=(MinLengthValidator(5),)
    )

    description = models.TextField(
        max_length=500,
        blank=False,
        null=False,
        validators=(MinLengthValidator(20),)
    )

    start_date = models.DateField(
        blank=False,
        null=False,
    )

    end_date = models.DateField(
        blank=False,
        null=False
    )

    rating = models.IntegerField(
        blank=False,
        null=False,
        validators=(MinValueValidator(1), MaxValueValidator(5))
    )

    budget = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    user = models.ForeignKey(to=AppUser, on_delete=models.CASCADE)
