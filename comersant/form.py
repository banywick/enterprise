from django import forms
from .models import Comment, Leading

class InputDataForm(forms.Form):
    invoice = forms.CharField(
        error_messages={'required': 'Не указан № накладной'},
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Номер накладной'}),
        label=''
    )
    date = forms.DateField(
        error_messages={'required': 'Выберите дату'},
        widget=forms.TextInput(attrs={'placeholder': 'Дата'}),
        label=''
    )
    supplier = forms.CharField(
        error_messages={'required': 'Не указан поставщик'},
        widget=forms.TextInput(attrs={'id': 'email_register_field', 'placeholder': 'Не выбран поставщик'}),
        label=''
    )
    article = forms.CharField(
        error_messages={'required': 'Введите артикул'},
        widget=forms.TextInput(attrs={'placeholder': 'Не введен артикул'}),
        label=''
    )
    auto_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Автоматическая подстановка наименования'}),
        label=''
    )
    auto_unit = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Автоматическая подстановка единицы'}),
        label=''
    )
    quantity = forms.IntegerField(
        error_messages={'required': 'Введите количество'},
        widget=forms.TextInput(attrs={'placeholder': 'Автоматическая подстановка единицы'}),
        label='Введите количество '
    )
    comment = forms.ModelChoiceField(
        queryset=Comment.objects.all(),
        error_messages={'required': 'Введите вариант'},
        widget=forms.Select(attrs={'placeholder': 'Выберите вариант'}),
        empty_label="Выберите вариант"
    )
    leading = forms.ModelChoiceField(
        queryset=Leading.objects.all(),
        error_messages={'required': 'Ведущий'},
        widget=forms.Select(attrs={'placeholder': 'Ведущий накладную'}),
        empty_label="Ведущий накладную"
    )