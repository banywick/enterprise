from django.urls import path
from comersant.views import input_data, shortfalls_view, edit_row_form,edit_status, delete_row


urlpatterns = [
    path('shortfalls/', shortfalls_view, name='shortfalls'),
    path('shortfalls/input-data/', input_data, name='input_data'),
    path('shortfalls/edit_row/<int:id>/', edit_row_form, name='edit_row'),
    path('shortfalls/edit_status/<int:id>/', edit_status, name='edit_status'),
    path('shortfalls/delete_row/<int:id>/', delete_row, name='delete_row'),
]