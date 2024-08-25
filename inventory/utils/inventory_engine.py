from django.db.models import F, Sum, Q, OuterRef, Subquery
from finder.models import Remains
from ..forms import InputValue
from ..models import RemainsInventory


# def get_inventory(request):
#     # unic_sum_posit = RemainsInventory.objects.values('article', 'title', 'base_unit')
#     form = InputValue(request.POST)
#     if request.method == 'POST':
#         query = Q()
#         if request.POST.get('input'):
#             values = request.POST['input'].split(' ')  # сбор значений с инпута
#             for element in values:
#                 if element:
#                     query =Q(title__icontains=element)
#             error_message = 'Товар не найден'
#             inventory = RemainsInventory.objects.filter(query)[:500]
#             if not inventory:
#                 inventory = RemainsInventory.objects.filter(article__icontains=values[0])

#             if not inventory.exists():  # если ничего не найдено из нескольких значений в инпуте
#                 return {'form': form, 'e_art_title': error_message}  # post если не найдено
#             return {'form': form, 'inventory': inventory}  # post
#     return {'form': form}  # get



def get_inventory(request):
    form = InputValue(request.POST)
    subquery = Remains.objects.filter(article=OuterRef('article')).values('article').annotate(total_quantity=Sum('quantity')).values('total_quantity')
    if request.method == 'POST':
        query = Q()
        input_value = request.POST.get('input')

        if input_value:
            # Создаем запрос для поиска по всем словам
            values = input_value.split()
            for element in values:
                if element:  # только непустые элементы
                    query |= Q(title__icontains=element)  # Объединяем условия через OR
            inventory = RemainsInventory.objects.filter(query).annotate(total_quantity=Subquery(subquery))[:50]

            if inventory.exists():
                return {'form': form, 'inventory': inventory}
            
            # Если ничего не найдено, пробуем искать по артикулу
            # Создаем подзапрос для суммирования quantity из Remains, где article соответствует статье из Remains
            inventory = RemainsInventory.objects.filter(article__icontains=values[0]).annotate(total_quantity=Subquery(subquery))
            if inventory.exists():
                return {'form': form, 'inventory': inventory}
        
        # Если ничего не нашли, возвращаем сообщение об ошибке
        error_message = 'Товар не найден'
        return {'form': form, 'e_art_title': error_message}

    return {'form': form}  # Если метод GET


