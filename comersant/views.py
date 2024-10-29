from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

from comersant.form import InputDataForm
from comersant.models import TableData

def shortfalls_view(request):
    form = InputDataForm()
    return render(request, 'comersant/comers.html',  {'form': form})

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
