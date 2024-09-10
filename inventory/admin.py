from django.contrib import admin
from finder.models import Remains
from .models import RemainsInventory, OrderInventory, CreationdDateInventory
from django.db import transaction


admin.site.register(CreationdDateInventory)

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
    list_display = ('article', 'title', 'base_unit', 'status')
    search_fields = ('article',)
    actions = ['set_status_to_new', 'set_status_to_old', 'delete_selected']

    @admin.action(description='Удалить выбранные записи')
    def delete_selected(self, request, queryset):
        with transaction.atomic():
            queryset.delete()
        self.message_user(request, 'Выбранные записи успешно удалены.')

    @admin.action(description='Установить статус "Сошлось"')
    def set_status_to_new(self, request, queryset):
        queryset.update(status='Сошлось')
        self.message_user(request, 'Статус выбранных объектов успешно обновлен на "Сошлось".')

    @admin.action(description='Установить статус "Перепроверить"')
    def set_status_to_old(self, request, queryset):
        queryset.update(status='Перепроверить')
        self.message_user(request, 'Статус выбранных объектов успешно обновлен на "Перепроверить".')

    @admin.action(description='Удалить статус')
    def remove_status(self, request, queryset):
        queryset.update(status=None)
        self.message_user(request, 'Статус выбранных объектов успешно удалён.')



    

@admin.register(OrderInventory)
class OrderInventoryModelAdmin(admin.ModelAdmin):
    list_display = (
        'get_user_name',
        'get_product_article',
        'get_product_title',
        'get_product_base_unit',
        'quantity_ord',
        'address', 'comment',
        'created_at',
        'get_product_status')

    def get_product_article(self, obj):
        return obj.product.article  
    get_product_article.short_description = 'Артикул'  # заголовок столбца

    def get_user_name(self, obj):
        return obj.user.username  
    get_user_name.short_description = 'Пользователь'  # заголовок столбца


    def get_product_title(self, obj):
        return obj.product.title 
    get_product_title.short_description = 'Название'  # заголовок столбца

    def get_product_base_unit(self, obj):
        return obj.product.base_unit 
    get_product_base_unit.short_description = 'Единица'  # заголовок столбца

    def get_product_status(self, obj):
        return obj.product.status 
    get_product_status.short_description = 'Статус'  # заголовок столбца
















