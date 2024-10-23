from django.urls import path
from comersant.views import shortfalls_view, data


urlpatterns = [
    path('shortfalls/', shortfalls_view, name='shortfalls'),
    path('data/', data, name='data'),
]