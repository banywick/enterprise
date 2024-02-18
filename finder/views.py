import os
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage

from config import settings
from finder.models import Remains
from celery.result import AsyncResult

from finder.tasks import data_save_db


def upload_file(request):
    if request.POST and request.FILES:
        doc = request.FILES.get("doc")
        if doc.content_type.startswith(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            upload_folder = FileSystemStorage(location="finder/document")
            file_name = upload_folder.save(doc, doc)
            file_url = os.path.join(settings.BASE_DIR) + "/finder/document/" + file_name
            task = data_save_db.delay(file_url)
            res = task.id
            request.session["celery_task_id"] = str(res)
            return redirect("home")
        else:
            print("отправить предупреждение")

    return render(request, "upload.html")


def get_home_page(request):
    model = Remains.objects.filter(quantity__lt=30, quantity__gt=20)
    celery_task_id = request.session.get("celery_task_id")
    print(AsyncResult(celery_task_id).state)

    # task_result = AsyncResult(id)
    # print(task_id)
    # task_result = AsyncResult(task_id)
    # print(task_result.state)
    context = {"model": model}
    return render(request, "index.html", context=context)


# result = AsyncResult(id_task)
#             print(result.state)
