from django.urls import path

from inventory.views import get_main_inventory



urlpatterns = [
    path('inventory/', get_main_inventory, name='inventory'),
    # path('detail-product/<str:article>', inventory_detail, name='inventory_detail'),
    
    # path('inventory/', get_main_inventory, name='inventory'),
    # path('detail-product/<str:article>', inventory_detail, name='inventory_detail'),
    # path('user_detaial/', user_detail, name='user_detail'),
    # path('edit/<int:id_row>', delete_row, name='delete'),
    # path('set_status/<str:status>/<str:article>/', set_status, name='set_status')

]