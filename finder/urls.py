from os import name
from django.urls import path
from .views import *
   
from .utils import clear_sort

urlpatterns = [
    path("login", get_access, name="login"),
    path("logout/", user_logout, name="logout"),
    path("upload/", upload_file, name="upload"),
    path("", search_engine, name="main"),
    path("check_task_status/", check_task_status, name="check_task_status"),
    path("choice/", choice_projects, name="choice"),
    path("clear/", clear_sort, name="clear"),
    path("details/<str:art>", get_details_product, name="details"),
    path('change_row/', change_row, name='change_row'),
    path("manual/", get_manual, name="manual"),
    path("sahr/", sahr, name="sahr"),
    path("check_article/<str:art>", check_article, name="check_article"),
    path("del_row_sahr/<int:id>", del_row_sahr, name='del_row_sahr'),
    # path('backup', backup_table, name='backup'),
    path('download-excel/', download_backup, name='dowload_backup'),
]

