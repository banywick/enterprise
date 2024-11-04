from django import forms
from .models import Comment, Leading, Supler, Specialist,Invoice

class InputDataForm(forms.Form):
    invoice = forms.CharField(
        error_messages={'required': 'Не указан № накладной'},
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Номер накладной'}),
        label='Накладная'
    )
    date = forms.DateField(
        error_messages={'required': 'Выберите дату'},
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата'
    )
    supplier = forms.ModelChoiceField(
        queryset=Supler.objects.all(),
        error_messages={'required': 'Не указан поставщик'},
        widget=forms.Select(attrs={'placeholder': 'Выберите вариант'}),
        empty_label="Выберите вариант",
        label='Поставщик'
    )
    article = forms.CharField(
        error_messages={'required': 'Введите артикул'},
        widget=forms.TextInput(attrs={'class':'check_article','placeholder': 'Артикул'}),
        label='Артикул'
    )
    auto_title = forms.CharField(
        widget=forms.TextInput(attrs={'class':'views_title','placeholder': 'Автоматическая подстановка наименования'}),
        label=''
    )
    quantity = forms.IntegerField(
        error_messages={'required': 'Введите количество'},
        widget=forms.TextInput(attrs={'placeholder': 'Количество'}),
        label='Введите количество '
    )
    comment = forms.ModelChoiceField(
        queryset=Comment.objects.all(),
        error_messages={'required': 'Введите вариант'},
        widget=forms.Select(attrs={'placeholder': 'Выберите вариант'}),
        empty_label="Выберите вариант",
        label='Коментарий по товару'
    )
    specialist = forms.ModelChoiceField(
        queryset=Specialist.objects.all(),
        error_messages={'required': 'Фамилия специалиста'},
        widget=forms.Select(attrs={'placeholder': 'Специалист'}),
        empty_label="Выберите вариант",
        label='Специалист на приемке'
    )
    leading = forms.ModelChoiceField(
        queryset=Leading.objects.all(),
        error_messages={'required': 'Ведущий'},
        widget=forms.Select(attrs={'placeholder': 'Ведущий накладную'}),
        empty_label="Ведущий накладную",
        label='Ведущий накладную'
    )
    hidden_unit = forms.CharField(
        widget=forms.HiddenInput(attrs={'id': 'hidden_unit'})  # Скрытое поле с id
    )
    hidden_article = forms.CharField(
        widget=forms.HiddenInput(attrs={'id': 'hidden_article'})  # Скрытое поле с id
    )



class InvoiceEditForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'date', 'supplier', 'article', 'name', 'unit', 'quantity', 'comment', 'specialist']
        labels = {
            'invoice_number': 'Номер накладной',
            'date': 'Дата',
            'supplier': 'Поставщик',
            'article': 'Артикул',
            'name': 'Наименование',
            'unit': 'Единица измерения',
            'quantity': 'Количество',
            'comment': 'Комментарий',
            'specialist': 'Специалист',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
class InvoiceEditFormStatus(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['status', 'description']
        labels = {
            'status': 'Статус',
            'description': 'Примечание',
        }

class FilterForm(forms.Form):
    supplier = forms.ModelChoiceField(
        queryset=Supler.objects.all(),
        required=False,
        widget=forms.Select(attrs={'placeholder': 'Выберите вариант'}),
        empty_label="Выберите вариант",
        label='Поставщик')
    leading = forms.ModelChoiceField(
        queryset=Leading.objects.all(),
        required=False,
        widget=forms.Select(attrs={'placeholder': 'Ведущий накладную'}),
        empty_label="Ведущий накладную",
        label='Ведущий накладную')
    

class AddSupplerForm(forms.ModelForm):
    class Meta:
        model = Supler
        fields = ['name']
        labels = {
            'name': 'Название',
        }
