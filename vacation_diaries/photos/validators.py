from django.core.exceptions import ValidationError


def max_file_size(image):
    if image.size > 8388608:
        raise ValidationError("You can upload pictures with size up to 8MB!")
