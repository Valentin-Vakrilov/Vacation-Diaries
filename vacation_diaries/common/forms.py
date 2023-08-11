from django import forms


class SearchForm(forms.Form):
    vacation = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Please enter a destination"
            }
        )
    )
