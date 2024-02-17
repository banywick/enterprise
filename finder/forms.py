from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


class LoadFileForm(forms.Form):
    file = forms.FileField(
        required=False, validators=[FileExtensionValidator(allowed_extensions=["xlsx"])]
    )

    def clean_file(self):
        file = self.cleaned_data.get("file")

        if file:
            if not file.content_type.startswith("application/vnd.ms-excel"):
                raise ValidationError("Допустимы только файлы Excel (XLS и XLSX).")
            return file
