from django.shortcuts import render
from inventory.utils.inventory_engine import get_inventory


def get_main_inventory(request):
    context = get_inventory(request)
    return render(request, 'inventory/inventory.html', context=context)


