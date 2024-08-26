from django.shortcuts import render
from inventory.utils.inventory_engine import get_inventory


def get_main_inventory(request):
    context = get_inventory(request)
    return render(request, 'inventory/inventory.html', context=context)




# def inventory_detail(request, article):
#     product = get_one_product(article)  # выбор первой позицци по артикулу для детализации
#     user_set_invent = get_user_set_invent(product)  # Фильтрация по выбору для всех пользователей
#     total_quantity_ord = get_total_quantity_ord(product)  # Посчитанно всеми пользователями
#     unic_sum_posit = get_unic_sum_posit(article)  # Остаток по инвентаризации

#     sum_remains_now = "{:.2f}".format(get_unic_sum_posit_remains_now(article))  # Текущий остаток
#     sum_remains_now = float(sum_remains_now)  # пеобразование 2 знака после точки
#     move_product = float(sum_remains_now) - float(
#         unic_sum_posit)  # текущий остаток минус остаток инвентаризации (движение)
#     move_product = "{:.2f}".format(move_product)
#     remains_sum = calculate_remains_sum(sum_remains_now,
#                                         total_quantity_ord)  # тек остаток минус сумма подсчета пользователями (Движение)
#     if remains_sum < 0:
#         alert_count = abs(remains_sum)
#     else:
#         alert_count = remains_sum

#     if request.method == 'POST':
#         quantity_ord = request.POST.get('quantity_set')
#         set_address = request.POST.get('address')
#         set_comment = request.POST.get('comment')
#         user = request.user

#         create_inventory_item(product, user, quantity_ord, set_address, set_comment)
#         return HttpResponseRedirect(reverse('inventory_detail', args=(article,)))
#     get_status = RemainsInventory.objects.filter(article=article).first().status

#     context = {'product': product, 'user_set_invent': user_set_invent,
#                'total_quantity_ord': total_quantity_ord, 'unic_sum_posit': unic_sum_posit, 'remains_sum': remains_sum,
#                'sum_remains_now': sum_remains_now, 'move_product': move_product, 'get_status': get_status,
#                'alert_count': alert_count}
#     return render(request, 'inventory_detail.html', context=context)


