from django.urls import path
from finder.views import search_engine
from inventory.utils.inventory_engine import inventory_detail
from inventory.views import get_main_inventory, get_inventory_detail, delete_row, set_status, user_detail, report_inventory



urlpatterns = [
    path('inventory/', get_main_inventory, name='inventory'),
    path('detail-product/<str:article>', get_inventory_detail, name='inventory_detail'),
    path('find/', search_engine, name='find'),
    path('edit/<int:id_row>', delete_row, name='delete'),
    path('set_status/<str:status>/<str:article>/', set_status, name='set_status'),
    path('user_detaial/', user_detail, name='user_detail'),
    path('report_inventory', report_inventory, name='report_inventory' ),
]