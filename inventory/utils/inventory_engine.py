from django.db.models import Sum, Q
from ..forms import InputValue
from ..models import RemainsInventory


def get_inventory(request):
    # unic_sum_posit = RemainsInventory.objects.values('article', 'title', 'base_unit')


    form = InputValue(request.POST)
    if request.method == 'POST':
        query = Q()
        if request.POST.get('input'):
            values = request.POST['input'].split(' ')  # сбор значений с инпута
            for element in values:
                if element:
                    query =Q(title__icontains=element)
                    print(query)
               

           
            error_message = 'Товар не найден'
            inventory = RemainsInventory.objects.filter(query)[:500] | Q(article__icontains=values)
            # inventory = unic_sum_posit.filter(query)[:500] | unic_sum_posit.filter(
            #     article__contains=request.POST['input'])
            if not inventory.exists():  # если ничего не найдено из нескольких значений в инпуте
                return {'form': form, 'e_art_title': error_message}  # post если не найдено
            return {'form': form, 'inventory': inventory}  # post
    return {'form': form}  # get