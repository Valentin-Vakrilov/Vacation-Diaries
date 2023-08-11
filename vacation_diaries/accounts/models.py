from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, EmailValidator
from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save


class AppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_FIELD = "username"
    USERNAME_MAX_LENGTH = 30

    objects = auth_models.UserManager()

    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        blank=False,
        null=False,
        validators=(MinLengthValidator(2),),
        error_messages={
            "unique": "A user with this username already exists. Please enter a different username!"
        }
    )

    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        validators=(EmailValidator(),),
        error_messages={
            "unique": "A user with this email is already registered. Please enter a different email address!"
        }
    )

    is_staff = models.BooleanField(default=False)


UserModel = get_user_model()


class Profile(models.Model):
    CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Diverse", "Diverse")
    )

    FIRST_NAME_MAX_LENGTH = 35
    LAST_NAME_MAX_LENGTH = 35

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        blank=True,
        null=True,
        validators=(MinLengthValidator(2),)
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        blank=True,
        null=True,
        validators=(MinLengthValidator(2),)
    )

    age = models.IntegerField(
        blank=True,
        null=True,
        validators=(MinValueValidator(0), MaxValueValidator(100))
    )

    gender = models.CharField(
        blank=True,
        null=True,
        choices=CHOICES
    )

    image = models.URLField(
        blank=True,
        null=True
    )

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )


@receiver(post_save, sender=AppUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
