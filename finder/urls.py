from django.urls import path
from .views import upload_file, check_task_status, search_engine, choice_projects
from .utils import clear_sort

urlpatterns = [
    path("upload/", upload_file, name="upload"),
    path("main/", search_engine, name="main"),
    path("check_task_status/", check_task_status, name="check_task_status"),
    path("choice/", choice_projects, name="choice"),
    path("clear/", clear_sort, name="clear"),
    
    # path("", get_access, name="login"),
    # path("main/", get_main_page, name="main"),
    # path("details/<int:id>", get_details_product, name="details"),
    # path("logout/", user_logout, name="logout"),
]
