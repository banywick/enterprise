from django.shortcuts import render
from inventory.utils.inventory_engine import get_inventory, inventory_detail


def get_main_inventory(request):
    context = get_inventory(request)
    return render(request, 'inventory/inventory.html', context=context)


def get_inventory_detail(request, article):
    context = inventory_detail(request, article)
    return render(request, 'inventory/inventory_detail.html', context=context)







