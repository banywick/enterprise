import copy
from django.contrib.auth import authenticate, login, logout
import os
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
import redis

from config import settings
from config.context_processors import get_file_name
from finder.forms import InputValue
from finder.models import Remains, UserIP
from celery.result import AsyncResult


from finder.tasks import data_save_db

from finder.utils import choice_project_dict, get_context_input_filter_all


def user_logout(request):
    logout(request)
    return redirect("main")


def get_access(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("main")
        else:
            context["error"] = "Неверное имя пользователя или пароль"
    if request.user.is_authenticated:
        return redirect("main")
    return render(request, "registration.html", context)


r = redis.StrictRedis(host="localhost", port=6379, db=0)


def upload_file(request):
    if request.POST and request.FILES:
        doc = request.FILES.get("doc")
        # Получение имени файла
        filename = doc.name
        # Сохранение в Redis
        r.set("file_name", filename)

        if doc.content_type.startswith(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            upload_folder = FileSystemStorage(location="finder/document")
            file_name = upload_folder.save(doc, doc)
            file_url = os.path.join(settings.BASE_DIR) + "/finder/document/" + file_name
            task = data_save_db.delay(file_url)
            request.session["task_id"] = ""
            task_id = AsyncResult(task.id)
            request.session["task_id"] = str(task_id)
        else:
            return render(
                request, "upload.html", {"error": "Выберите пожалуйста тип файла *xlsx"})
    return render(request, "upload.html")


def search_engine(request):
    ip = request.META.get('REMOTE_ADDR')
    name = request.META.get('USERNAME')
    UserIP.objects.get_or_create(ip_address=ip, name=name)
    request.session["task_id"] = ""

    context = get_context_input_filter_all(request)
    return render(request, "index.html", context=context)


def choice_projects(request):
    context = choice_project_dict(request)
    if request.method == "POST":
        return redirect("main")
    return render(request, "choice_project.html", context=context)


def get_details_product(request, id):
    details = Remains.objects.filter(id=id)
    if not details:
        return JsonResponse({"error": "Детали не найдены"})

    detail = details.first()
    article = detail.article
    unit = detail.base_unit
    title = detail.title

    det = Remains.objects.filter(article=article)
    sum_art = sum(float(d.quantity) for d in det)
    sum_art_str = f"{sum_art:.2f} {unit}"
    proj_quan_unit = []
    for p in det:
        proj_quan_unit.append(f"{p.project} -- {p.quantity} {p.base_unit}")

    return JsonResponse(
        {
            "title": "Детализация",
            "project": proj_quan_unit,
            "sum": sum_art_str,
            "art": article,
            "title": title,
        }
    )


def check_task_status(request):
    task_id = request.session.get("task_id")  # Получите идентификатор задачи из запроса
    if task_id == "":
        return JsonResponse({"status": "unknown"})
    else:
        task_id = request.session.get("task_id")
        task_result = AsyncResult(task_id)
        if task_result.state == "SUCCESS":
            return JsonResponse({"status": "success"})
        elif task_result.state == "FAILURE":
            return JsonResponse({"status": "failure"})
        elif task_result.state == "PENDING":
            return JsonResponse({"status": "pending"})
        
        
def get_manual(request):
    return render(request, 'manual.html')
