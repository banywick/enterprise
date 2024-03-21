import copy
from re import T
from django.contrib.auth import authenticate, login, logout
import os
from django.db.models import F, Q, Func, Sum, Value
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
import redis

from config import settings
from config.context_processors import get_file_name
from finder.forms import InputValue
from finder.models import Data_Table, Remains, UserIP
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
                request, "upload.html", {"error": "Выберите пожалуйста тип файла *xlsx"}
            )
    return render(request, "upload.html")


def search_engine(request):
    ip = request.META.get("REMOTE_ADDR")
    name = request.META.get("USERNAME")
    if ip or name:
        UserIP.objects.get_or_create(ip_address=ip, name=name)
    request.session["task_id"] = ""

    context = get_context_input_filter_all(request)
    return render(request, "index.html", context=context)


def choice_projects(request):
    context = choice_project_dict(request)
    if request.method == "POST":
        return redirect("main")
    return render(request, "choice_project.html", context=context)


def get_details_product(request, art):
    details = Remains.objects.filter(article__contains=art)
    if not details:
        return JsonResponse({"error": "Товар отсутствует в базе"})

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
    return render(request, "manual.html")



def sahr(request):
    all_remains_art = Remains.objects.all().values_list('article', flat=True).distinct('article')
    all_remains_art = list(map(str, all_remains_art)) # Преобразовываем все в трочное значение
    Data_Table.objects.exclude(article__in=all_remains_art).update(index_remains=None)
    if request.method == 'POST':

        if 'search_sahr_form' in request.POST:
            value_input = request.POST.get('value_input')
            article = Q(article__contains=value_input)
            address = Q(address__icontains=value_input)
            party = Q(party__icontains=value_input)
            result_search = Data_Table.objects.filter(article | address | party)
            if not result_search.exists():
                error_search = 'Ничего не найдено'
                return render(request, "sahr.html", {'error_search': error_search})
            return render(request, "sahr.html", {'data_table': result_search})
        
        if 'save_button_form' in request.POST:
            remains_id = request.POST.get("id")
            address = request.POST.get("address")
            comment = request.POST.get("comment")
            party = request.POST.get("select")
            remains = Remains.objects.get(id=remains_id)
            article = remains.article
            title = remains.title
            base_unit = remains.base_unit
            data_table = Data_Table(
                article=article,
                title=title,
                base_unit=base_unit,
                comment=comment,
                party=party,
                address=address,)
        
            part_address = Data_Table.objects.filter(Q(party=party) & Q(address=address))
            if part_address.exists():
                error_save = "На этом адресе такая позиция существует!"
                return render(request, "sahr.html", {"data_table": Data_Table.objects.all(), "error_save": error_save})
            else:
                data_table.save()
                return render(request, "sahr.html", {"data_table": Data_Table.objects.all()})
            
        
 
    return render(request, "sahr.html", {"data_table": Data_Table.objects.all()})
    


def sahr_table(request):
    return render(request, "sahr.html", {"data_table": Data_Table.objects.all()})



def del_row_shhr(request, id):
    Data_Table.objects.filter(id=id).delete()
    return redirect("sahr")

    


def check_article(request, art):
    article = Remains.objects.filter(article__icontains=art).first()
    total_quantity = Remains.objects.filter(article=article).aggregate(sum_quantity=Sum('quantity'))['sum_quantity']
    if article:
        all_party = Remains.objects.filter(article=article)
        party = {}
        for i, p in enumerate(all_party):
            party[i] = p.party
        title = article.title
        id = article.id
        total_quantity = f'{total_quantity:.2f}'
        return JsonResponse({"title": title, "id": id, "party": party, 'total_quantity': total_quantity})
    return JsonResponse({"error": "Товара нет в базе"})




