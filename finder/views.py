import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from config import settings


from finder.tasks import data_save_db, delete_file


def upload_file(request):
    if request.POST and request.FILES:
        doc = request.FILES.get("doc")
        if doc.content_type.startswith(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            upload_folder = FileSystemStorage(location="finder/document")
            file_name = upload_folder.save(doc, doc)
            file_url = os.path.join(settings.BASE_DIR) + "/finder/document/" + file_name
            data_save_db(file_url)
            delete_file(file_url)
        else:
            print("хуня")

    return render(request, "upload.html")
