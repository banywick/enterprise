from django.shortcuts import render


def get_main_inventory(request):
    # context = get_inventory(request)
    return render(request, 'inventory/inventory.html')