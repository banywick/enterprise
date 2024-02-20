from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


class InputValue(forms.Form):
    input = forms.CharField(
        label="",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Искать здесь...."}),
    )
