from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

from comersant.form import InputDataForm
from comersant.models import Invoice, TableData

def shortfalls_view(request):
    form = InputDataForm()
    return render(request, 'comersant/comers.html',  {'form': form})

def input_data(request):
    if request.method == 'POST':
        form = InputDataForm(request.POST)
        if form.is_valid():
            invoice = Invoice(
                invoice_number=form.cleaned_data['invoice'],
                date=form.cleaned_data['date'],
                supplier=form.cleaned_data['supplier'],
                article=form.cleaned_data['article'],
                name=form.cleaned_data['auto_title'],
                unit='шт',  # Пример значения, можно изменить
                quantity=form.cleaned_data['quantity'],
                comment=form.cleaned_data['comment'],
                manager=form.cleaned_data['leading']
            )
            invoice.save()
            return JsonResponse({'status': 'success', 'data': form.cleaned_data})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = InputDataForm()
    return render(request, 'input_data.html', {'form': form})










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
