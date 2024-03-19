from os import name
from django.urls import path
from .views import (
    upload_file,
    check_task_status,
    search_engine,
    choice_projects,
    get_access,
    user_logout,
    get_details_product,
    get_manual,
    sahr,
    check_article,
    del_row_shhr
)
from .utils import clear_sort

urlpatterns = [
    path("login", get_access, name="login"),
    path("logout/", user_logout, name="logout"),
    path("upload/", upload_file, name="upload"),
    path("", search_engine, name="main"),
    path("check_task_status/", check_task_status, name="check_task_status"),
    path("choice/", choice_projects, name="choice"),
    path("clear/", clear_sort, name="clear"),
    path("details/<int:id>", get_details_product, name="details"),
    path("manual/", get_manual, name="manual"),
    path("sahr/", sahr, name="sahr"),
    path("check_article/<str:art>", check_article, name="check_article"),
    path("del_row_shhr/<int:id>", del_row_shhr, name='del_row_shhr')
]
