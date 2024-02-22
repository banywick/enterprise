import json
from django.contrib.auth import authenticate, login, logout
import os
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage

from config import settings
from finder.models import Remains
from celery.result import AsyncResult

from finder.tasks import data_save_db
from celery.app.control import Inspect

from finder.utils import choice_project_dict, get_context_input_filter_all


def user_logout(request):
    logout(request)
    return redirect("login")


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


def upload_file(request):
    if request.POST and request.FILES:
        doc = request.FILES.get("doc")
        file_name = request.session["file_name"] = str(doc)
        if doc.content_type.startswith(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            upload_folder = FileSystemStorage(location="finder/document")
            file_name = upload_folder.save(doc, doc)
            file_url = os.path.join(settings.BASE_DIR) + "/finder/document/" + file_name
            task = data_save_db.delay(file_url)
            # task_result = AsyncResult(task.id).state
            # celery_task_id = request.session['result'] = str(task_result)
            # print(task_result)
        else:
            print("отправить предупреждение")
    return render(request, "upload.html")


def search_engine(request):
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
    pass
    # i = Inspect()
    # b = i.active()  # вернет все активные таски
    # c = i.registered()
    # return JsonResponse({"status": c})


# celery_task_id = request.session.get("celery_task_id")
# task_result = AsyncResult(celery_task_id)
# if task_result.state == "SUCCESS":
#     return JsonResponse({"status": "success"})
# elif task_result.state == "FAILURE":
#     return JsonResponse({"status": "failure"})
# elif task_result.state == "PENDING":
#     return JsonResponse({"status": "pending"})
# else:
#     return JsonResponse({"status": "unknown"})
