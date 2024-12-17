from mimetypes import guess_type
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from finder.tasks import backup_inventory_table
from inventory.utils.inventory_engine import create_inventory_item, get_inventory, inventory_detail
from .models import OrderInventory, RemainsInventory
from django.contrib.auth.decorators import login_required
from django.contrib import messages




@login_required
def get_main_inventory(request):
    try:
        context = get_inventory(request)
        return render(request, 'inventory/inventory.html', context=context)
    except ZeroDivisionError as e:
        messages.warning(request, "Произошла ошибка! Данные для инвентаризации не загружены.")
        return redirect('main')
    

@login_required
def get_inventory_detail(request, article):
    context = inventory_detail(request, article)
    return render(request, 'inventory/inventory_detail.html', context=context)

@login_required
def delete_row(request, id_row):
    """Ударяем строку в детализации. Если все удалено меняется статус"""
    order = OrderInventory.objects.get(id=id_row)
    order.delete()
    article = order.product.article
    if not OrderInventory.objects.filter(product=order.product ).exists(): 
        RemainsInventory.objects.filter(article=article).update(status=None)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
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
        if not OrderInventory.objects.filter(product=product).exists():
            create_inventory_item(product, user, quantity_ord, address, comment)


        elif OrderInventory.objects.filter(product=product).exists():
            print(22)
            if context.get('remains_sum') != 0:
                remains_in_context = context.get('remains_sum')
                quantity_ord = remains_in_context
                create_inventory_item(product, user, quantity_ord, address, comment)
        
            
    return redirect('inventory_detail', article=article)        

@login_required
def user_detail(request):
    order = OrderInventory.objects.select_related('product').filter(user=request.user).order_by('created_at')
    order_count = order.values('product_id').distinct().count()
    print(order_count)
    return render(request, 'inventory/user_detail.html', {'order': order, 'order_count': order_count})

@login_required
def report_inventory(request):
    file_path, file_name = backup_inventory_table()  # Однократный вызов функции
    # Определение MIME-типа файла
    mime_type, _ = guess_type(file_path)
    # Отправка файла как HTTP-ответ
    with open(file_path, 'rb') as file:
        response = HttpResponse(file, content_type=mime_type)
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response





