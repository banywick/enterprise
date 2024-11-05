from django.urls import path
from comersant.views import *


urlpatterns = [
    path('shortfalls/', shortfalls_view, name='shortfalls'),
    path('shortfalls/input-data/', input_data, name='input_data'),
    path('shortfalls/edit_row/<int:id>/', edit_row_form, name='edit_row'),
    path('shortfalls/edit_status/<int:id>/', edit_status, name='edit_status'),
    path('shortfalls/delete_row/<int:id>/', delete_row, name='delete_row'),
    path('shortfalls/filter/', add_session_filter, name='filter'),
    path('shortfalls/add_suppler/', add_suppler, name='add_suppler'),
    path('shortfalls/clear_filter/', clear_filter, name='clear_filter'),
]