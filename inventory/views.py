from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from inventory.utils.inventory_engine import create_inventory_item, get_inventory, inventory_detail
from .models import OrderInventory, RemainsInventory


def get_main_inventory(request):
    context = get_inventory(request)
    return render(request, 'inventory/inventory.html', context=context)


def get_inventory_detail(request, article):
    context = inventory_detail(request, article)
    return render(request, 'inventory/inventory_detail.html', context=context)


def delete_row(request, id_row):
    """Ударяем строку в детализации. Если все удалено меняется статус"""
    order = OrderInventory.objects.get(id=id_row)
    order.delete()
    article = order.product.article
    if not OrderInventory.objects.filter(product=order.product ).exists(): 
        RemainsInventory.objects.filter(article=article).update(status=None)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def set_status(request, status, article):
    """Меняем статус кнопками и при нажатии на кнопку Сошлось австоматически формируется экземпляр"""
    RemainsInventory.objects.filter(article=article).update(status=status) # Меняем статус
    context = inventory_detail(request, article) # Контекст с данными с детализации
    remains_in_context = context.get('remains_product') # получаем с контекста остаток
    for i in remains_in_context:
        quantity_ord = i.total_quantity # получили остаток
    product = context.get('product') # Экземпляр можели из контекста
    user = request.user
    address=''
    comment=''
    if status == 'Сошлось':
        # Проверяем, существует ли уже запись в InventoryItem для данного продукта и пользователя
        if not OrderInventory.objects.filter(product=product ,address=address,comment=comment ).exists():
            create_inventory_item(product, user, quantity_ord, address, comment)
        if not OrderInventory.objects.filter(product=product, user=user,address=address,comment=comment ).exists():
            RemainsInventory.objects.filter(article=article).update(status=None)
            
    return redirect('inventory_detail', article=article)        


def user_detail(request):
    order = OrderInventory.objects.select_related('product').filter(user=request.user)
    # order_count = OrderInventory.objects.values('product_id').distinct().count()
    order_count = order.values('product_id').distinct().count()
    print(order_count)
    return render(request, 'inventory/user_detail.html', {'order': order, 'order_count': order_count})





