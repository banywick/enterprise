from django.db.models import Sum, Q
from ..forms import InputValue
from ..models import RemainsInventory


def get_inventory(request):
    unic_sum_posit = RemainsInventory.objects.values('article', 'title', 'base_unit')


    form = InputValue(request.POST)
    if request.method == 'POST':
        if request.POST.get('input'):
            values = request.POST['input'].split(' ')  # сбор значений с инпута
            values += [''] * (4 - len(values))  # Добавляем пустые строки, если введено менее четырех слов
            query = Q(title__icontains=values[0]) & Q(title__icontains=values[1]) & Q(title__icontains=values[2]) & Q(
                title__icontains=values[3])
            error_message = 'Товар не найден'
            inventory = unic_sum_posit.filter(query) | unic_sum_posit.filter(
                article__contains=request.POST['input'])
            if not inventory.exists():  # если ничего не найдено из нескольких значений в инпуте
                return {'form': form, 'e_art_title': error_message}  # post если не найдено
            return {'form': form, 'inventory': inventory}  # post
    return {'form': form}  # get