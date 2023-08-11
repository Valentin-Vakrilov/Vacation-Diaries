from django import forms
from .models import Vacation


class VacationForm(forms.ModelForm):
    class Meta:
        model = Vacation
        exclude = ["user"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"})
        }
