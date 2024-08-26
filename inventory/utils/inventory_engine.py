from django.db.models import F, Sum, Q, OuterRef, Subquery
from finder.models import Remains
from ..forms import InputValue
from ..models import RemainsInventory, OrderInventory
from django.http import HttpResponseRedirect
from django.urls import reverse


subquery = Remains.objects.filter(article=OuterRef('article')).values('article').annotate(total_quantity=Sum('quantity')).values('total_quantity')
def get_inventory(request):
    form = InputValue(request.POST)
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




def get_one_product(article):
    x = RemainsInventory.objects.filter(article=article).annotate(total_quantity=Subquery(subquery))
    return x


# def get_user_set_invent(product):
#     return OrderInventory.objects.filter(product=product)


# def get_total_quantity_ord(product):
#     total = OrderInventory.objects.filter(product=product).aggregate(total=Sum('quantity_ord'))['total']
#     return total if total is not None else 0


# def get_unic_sum_posit(article):
#     return RemainsInventory.objects.filter(article=article).aggregate(sum_art=Sum('quantity'))['sum_art']


# def get_unic_sum_posit_remains_now(article):  # остаток по последнему загруженному документу
#     if Remains.objects.filter(article__icontains=article).aggregate(sum_art_rem_now=Sum('quantity'))[
#         'sum_art_rem_now'] == None:
#         return 0
#     return Remains.objects.filter(article__icontains=article).aggregate(sum_art_rem_now=Sum('quantity'))[
#         'sum_art_rem_now']


# def calculate_remains_sum(sum_remains_now, total_quantity_ord):  # Осталось посчитать
#     if sum_remains_now == None:  # если нет позиции в таблице остатки (Remains)
#         sum_remains_now = 0
#     result = float(sum_remains_now) - float(total_quantity_ord)
#     return result


def create_inventory_item(product, user, quantity_ord, address, comment):
    inventory_item = OrderInventory.objects.create(
        product=product,
        user=user,
        quantity_ord=quantity_ord,
        address=address,
        comment=comment)
    inventory_item.save()



def inventory_detail(request, article):
    product = get_one_product(article)  # выбор первой позицци по артикулу для детализации
    for pr in product:
        print(pr)
    # user_set_invent = get_user_set_invent(product)  # Фильтрация по выбору для всех пользователей
    # total_quantity_ord = get_total_quantity_ord(product)  # Посчитанно всеми пользователями
    # unic_sum_posit = get_unic_sum_posit(article)  # Остаток по инвентаризации

    # sum_remains_now = "{:.2f}".format(get_unic_sum_posit_remains_now(article))  # Текущий остаток
    # sum_remains_now = float(sum_remains_now)  # пеобразование 2 знака после точки
    # move_product = float(sum_remains_now) - float(
    #     unic_sum_posit)  # текущий остаток минус остаток инвентаризации (движение)
    # move_product = "{:.2f}".format(move_product)
    # remains_sum = calculate_remains_sum(sum_remains_now,
    #                                     total_quantity_ord)  # тек остаток минус сумма подсчета пользователями (Движение)
    # if remains_sum < 0:
    #     alert_count = abs(remains_sum)
    # else:
    #     alert_count = remains_sum

    if request.method == 'POST':
        quantity_ord = request.POST.get('quantity_set')
        set_address = request.POST.get('address')
        set_comment = request.POST.get('comment')
        user = request.user

        create_inventory_item(product, user, quantity_ord, set_address, set_comment)
        return HttpResponseRedirect(reverse('inventory_detail', args=(article,)))
    # get_status = RemainsInventory.objects.filter(article=article).status

    context = {'product': product}
    return context    