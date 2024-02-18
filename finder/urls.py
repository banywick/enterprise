from django.urls import path
from .views import upload_file, get_home_page

urlpatterns = [
    path("upload/", upload_file, name="upload"),
    path("", get_home_page, name="home"),
]
