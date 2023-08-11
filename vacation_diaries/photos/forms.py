from django import forms
from .models import Photo, Comment


def get_vacation_label(vacation):
    return vacation.destination


class PhotoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["vacation"].label_from_instance = get_vacation_label

    class Meta:
        model = Photo
        exclude = ["user", "likes", "total_likes"]


class PhotoEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["vacation"].label_from_instance = get_vacation_label

    class Meta:
        model = Photo
        fields = ["description", "vacation"]


class PhotoCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_text"]
