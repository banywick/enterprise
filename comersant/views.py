from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
import json

from comersant.form import InputDataForm
from comersant.models import Invoice

def shortfalls_view(request):
    form = InputDataForm()
    invoices = Invoice.objects.all()  # Получаем все объекты модели Invoice
    context = {
        'form': form,
        'invoices': invoices
    }
    return render(request, 'comersant/comers.html', context)

def input_data(request):
    if request.method == 'POST':
        form = InputDataForm(request.POST)
        if form.is_valid():
            invoice = Invoice(
                invoice_number=form.cleaned_data['invoice'],
                date=form.cleaned_data['date'],
                supplier=form.cleaned_data['supplier'],
                article=form.cleaned_data['hidden_article'],
                name=form.cleaned_data['auto_title'],
                unit=form.cleaned_data['hidden_unit'],  # Пример значения, можно изменить
                quantity=form.cleaned_data['quantity'],
                comment=form.cleaned_data['comment'],
                specialist=form.cleaned_data['specialist'],
                leading=form.cleaned_data['leading']
            )
            invoice.save()
            return redirect('shortfalls')
    










@csrf_exempt
def data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        row = data['row']
        col = data['col']
        value = data['value']

        TableData.objects.update_or_create(row=row, col=col, defaults={'value': value})

        return JsonResponse({'status': 'success'})

    elif request.method == 'GET':
        data = TableData.objects.all().values('row', 'col', 'value')
        return JsonResponse(list(data), safe=False)
