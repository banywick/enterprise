from django.contrib import admin
from finder.models import Remains
from .models import RemainsInventory
from django.db import transaction

@admin.register(Remains)
class RemainsModelAdmin(admin.ModelAdmin):
    list_display = ('article', 'title', 'base_unit', 'quantity')
    # list_display_links = ('Артикул', 'Название', 'Единица', 'Количество')
    search_fields = ('article',)
    actions = ['copy_to_inventory']

    def copy_to_inventory(self, request, queryset):
        unique_objs = {}
        
        # Собираем уникальные объекты на основе поля, по которому вы хотите делать проверку
        for obj in queryset:
            unique_key = (obj.article, obj.title, obj.base_unit)
            # Если уникальный ключ еще не добавлен, добавляем его в словарь
            if unique_key not in unique_objs:
                unique_objs[unique_key] = {
                    'article': obj.article,
                    'title': obj.title,
                    'base_unit': obj.base_unit
                }

        # Подготовка для batch insert/update
        remains_inventory_bulk = []
        
        for unique_obj in unique_objs.values():
            remains_inventory_bulk.append(RemainsInventory(**unique_obj))

        # Используйте transaction.atomic для обеспечения целостности данных
        with transaction.atomic():
            # Выполнение bulk_create
            RemainsInventory.objects.bulk_create(remains_inventory_bulk)

        self.message_user(request, "Данные успешно скопированы в Инвентаризацию.")
    copy_to_inventory.short_description = "Скопировать в Инвентаризацию"



@admin.register(RemainsInventory) 
class RemainsInventoryModelAdmin(admin.ModelAdmin):
    list_display = ('article','title','base_unit') 
    search_fields = ('article',) 




