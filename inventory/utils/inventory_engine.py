from django.db.models import Sum, Q, OuterRef, Subquery
from finder.models import Remains
from ..forms import InputValue
from ..models import RemainsInventory, OrderInventory


subquery = Remains.objects.filter(article=OuterRef('article')).values('article').annotate(total_quantity=Sum('quantity')).values('total_quantity')

def get_inventory(request):
    form = InputValue(request.POST)
    count_row = RemainsInventory.objects.values('article').distinct().count()  # количество уникальных строк
    not_empty_row = RemainsInventory.objects.filter(status='Сошлось').count()  # отмеченные как Сошлось
    remainder_row = count_row - not_empty_row # Посчитанные позиции
    percentage = f'{(not_empty_row / count_row) * 100:.2f}%' # выполненно процентов
    if request.method == 'POST':
        if request.POST.get('marker') == 'сошлось':
            inventory = RemainsInventory.objects.filter(status='Сошлось')
            return {'form': form, 'inventory': inventory, 'count_row': count_row, 'not_empty_row': not_empty_row,
                    'remainder_row': remainder_row, 'percentage': percentage}
        
        if request.POST.get('marker') == 'в работе':
            inventory = RemainsInventory.objects.filter(status='В работе')
            return {'form': form, 'inventory': inventory, 'count_row': count_row, 'not_empty_row': not_empty_row,
                    'remainder_row': remainder_row, 'percentage': percentage}
        
        if request.POST.get('marker') == 'перепроверить':
            inventory = RemainsInventory.objects.filter(status='Перепроверить')
            return {'form': form, 'inventory': inventory, 'count_row': count_row, 'not_empty_row': not_empty_row,
                    'remainder_row': remainder_row, 'percentage': percentage}
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
                return {'form': form, 'inventory': inventory, 'count_row': count_row, 'not_empty_row': not_empty_row,
                    'remainder_row': remainder_row, 'percentage': percentage}
            
            # Если ничего не найдено, пробуем искать по артикулу
            # Создаем подзапрос для суммирования quantity из Remains, где article соответствует статье из Remains
            inventory = RemainsInventory.objects.filter(article__icontains=values[0]).annotate(total_quantity=Subquery(subquery))
            if inventory.exists():
                for i in inventory:
                    if i.total_quantity == None:
                        i.total_quantity = 0
                return {'form': form, 'inventory': inventory, 'count_row': count_row, 'not_empty_row': not_empty_row,
                    'remainder_row': remainder_row, 'percentage': percentage}
        
        # Если ничего не нашли, возвращаем сообщение об ошибке
        error_message = 'Товар не найден'
        return {'form': form, 'e_art_title': error_message}

    return {'form': form,
            'count_row': count_row,
            'not_empty_row': not_empty_row,
            'remainder_row': remainder_row,
            'percentage': percentage}  # Если метод GET


def get_total_quantity_ord(product):
    total = OrderInventory.objects.filter(product=product).aggregate(total=Sum('quantity_ord'))['total']
    return total if total is not None else 0


def create_inventory_item(product, user, quantity_ord, address, comment):
    inventory_item = OrderInventory.objects.create(
        product=product,
        user=user,
        quantity_ord=quantity_ord,
        address=address,
        comment=comment)
    inventory_item.save()



def inventory_detail(request, article):
    product = RemainsInventory.objects.get(article=article) # Экземпляр из бд
    if request.method == 'POST':
        quantity_ord = request.POST.get('quantity_set')
        set_address = request.POST.get('address')
        set_comment = request.POST.get('comment')
        user = request.user
        create_inventory_item(product, user, quantity_ord, set_address, set_comment)
        RemainsInventory.objects.filter(article=article).update(status='В работе')


    remains_product = RemainsInventory.objects.filter(article=article).annotate(total_quantity=Subquery(subquery)) # остаток на сегодня
    user_set_invent =  OrderInventory.objects.filter(product=product)  # Фильтрация по выбору для всех пользователей
    total_quantity_ord = get_total_quantity_ord(product)  # Посчитанно всеми пользователями
    for r in remains_product:
        remains_sum =  float(r.total_quantity) - float(total_quantity_ord)
        if remains_sum < 0:
            alert_count = abs(remains_sum)
        else:
            alert_count = remains_sum
    get_status = RemainsInventory.objects.filter(article=article).first().status
    context = {'product': product,
                'user_set_invent':user_set_invent,
                'remains_product': remains_product,
                'total_quantity_ord': total_quantity_ord,
                'remains_sum' : remains_sum,
                'alert_count': alert_count,
                'get_status': get_status,
                
                }
    return context    