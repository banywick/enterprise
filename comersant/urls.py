from django.urls import path
from comersant.views import input_data, shortfalls_view


urlpatterns = [
    path('shortfalls/', shortfalls_view, name='shortfalls'),
    path('input-data/', input_data, name='input_data'),
]