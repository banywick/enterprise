import os

from django.contrib import messages
from config import settings
from datetime import datetime
from mimetypes import guess_type
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from finder.forms import ReviewForm
from finder.models import *
from celery.result import AsyncResult
from finder.tasks import backup_sahr_table, data_save_db
from finder.utils import choice_project_dict, connect_redis, get_context_input_filter_all
from django.contrib.auth.decorators import login_required


def user_logout(request):
    """Выход"""
    logout(request)
    return redirect("main")

def get_access(request):
    """Логин"""
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



@login_required
def upload_file(request):
    """Загрузка документа для обновления"""
    if request.POST and request.FILES:
        doc = request.FILES.get("doc")
        if doc.content_type.startswith(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"):
            upload_folder = FileSystemStorage(location="finder/document")
            file_name = upload_folder.save(doc, doc)
            file_url = os.path.join(settings.BASE_DIR) + "/finder/document/" + file_name
            task = data_save_db.delay(file_url)
            return render(request, 'upload.html', {'task_id': task.id})
        else:
            return render(
                request, "upload.html", {
                    "error": "Выберите пожалуйста тип файла *xlsx",
                    'task_id': 'unknown'}
            )
    return render(request, "upload.html", {'task_id': 'unknown'})


def check_task_status(request, task_id):
    """Получение статуса задачи"""
    if task_id == 'unknown' :
        return JsonResponse({"status": 'unknown'})
    else:
        async_result = AsyncResult(task_id)
        if async_result.status == "SUCCESS":
            date_update_document = datetime.now().date().strftime('%d.%m.%Y')
            connect_redis().set("file_name", date_update_document)
        return JsonResponse({"status": async_result.status})


def search_engine(request):
    """Логика поисковика собирается вся в контекст"""
    context = get_context_input_filter_all(request)
    return render(request, "index.html", context=context)


def choice_projects(request):
    """Выбор проекта"""
    context = choice_project_dict(request)
    if request.method == "POST":
        return redirect("main")
    return render(request, "choice_project.html", context=context)
    
    
def get_details_product(request, art):
    """Детализация позиции при переходе по ссылке"""
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
        {"title": "Детализация",
        "project": proj_quan_unit,
        "sum": sum_art_str,
        "art": article,
        "title": title,
        })


def get_manual(request):
    """Инструкция для поисковика"""
    return render(request, "manual.html")

@login_required
def sahr(request):
    """Логика С.А.ХР (Система Адресного Хранения)"""
    count_row = Data_Table.objects.all().count()
    all_remains_art = Remains.objects.all().values_list('article', flat=True).distinct()
    all_remains_art = list(map(str, all_remains_art)) # Преобразовываем все в строчное значение
    Data_Table.objects.filter(article__in=all_remains_art).update(index_remains=2)
    if request.method == 'POST':
        if 'search_sahr_form' in request.POST:
            value_input = request.POST.get('value_input')

            if str(value_input).startswith('d'):
                value_input =str(value_input).split(' ')
                if len(value_input) == 2:
                    deleted = Deleted.objects.filter(article__icontains=value_input[1])
                    info = 'Закрыть историю удаленных строк'
                    return render(request, "sahr.html", {'data_table': deleted,  'info': info})

            def check_ru_symbol(): # все русские переводим в англисские
                replacements = {
                    'а': 'a',
                    'б': 'b',
                    'в': 'b',
                    'с': 'c',
                    'д': 'd',
                    'е': 'e',
                    'ф': 'f',
                    'н': 'h'
                }
                return ''.join(replacements.get(char.lower(), char) for char in value_input)
            def find_en_ru():
                replacements = {
                    'a': 'а',
                    'b': 'б',
                    'b': 'в',
                    'c': 'с',
                    'd': 'д',
                    'e': 'е',
                    'f': 'ф',
                    'h': 'н'
                }
                return ''.join(replacements.get(char.lower(), char) for char in value_input)
            article = Q(article__contains=value_input)
            address_ru = Q(address__icontains=check_ru_symbol())
            address_en = Q(address__icontains=find_en_ru())
            party = Q(party__icontains=value_input)
            result_search = Data_Table.objects.filter(article | party | address_ru | address_en)[:50]
            if not result_search.exists():
                error_search = 'Ничего не найдено'
                return render(request, "sahr.html", {'error_search': error_search})
            if value_input == "":
                Data_Table.objects.all().order_by("-id")[:50][::-1]
            else:    
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
                address=address,
                date=datetime.now())
            part_address = Data_Table.objects.filter(Q(party=party) & Q(address=address))
            if part_address.exists():
                error_save = "На этом адресе такая позиция существует!"
                return render(request, "sahr.html", {"data_table":Data_Table.objects.all().order_by("-id")[:50][::-1], "error_save": error_save,  'count_row':count_row})
            else:
                data_table.save()
                return render(request, "sahr.html", {"data_table": Data_Table.objects.all().order_by("-id")[:50][::-1], 'count_row':count_row})
    # doc_sahr() #функция сохранения в базу исходника САХР
    return render(request, "sahr.html", {"data_table":  Data_Table.objects.all().order_by("-id")[:50][::-1], 'count_row':count_row})
    


def change_row(request):
    """Редактирование строк в таблице на фронте"""
    id_data_table = request.POST.get('id_data_table')
    address =  request.POST.get('address')
    comment =  request.POST.get('comment')
    data_table_entry = Data_Table.objects.get(id=id_data_table)
    if address:
        data_table_entry.address = address
        data_table_entry.save(update_fields=['address'])
    if comment:
        data_table_entry.comment = comment
        data_table_entry.save(update_fields=['comment'])
    return redirect('sahr')


def get_history(request, id):
    """История удаленных файлов"""
    data_table = History.objects.filter(data_table_id=id).order_by('date')
    info = 'Закрыть историю'
    return render(request, "sahr.html", {"data_table": data_table, 'info': info})



def del_row_sahr(request, id):
    """Удаляет строку по id"""
    Data_Table.objects.filter(id=id).delete()
    return redirect("sahr")



def check_article(request, art):
    """Провекра для САХР есть ли такой артикул в базе"""
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



def download_backup(request):
    """Загрузка резервной копии на локальный компьютер"""
    file_path = backup_sahr_table()[0]
    # Определение MIME-типа файла
    mime_type, _ = guess_type(file_path)
    # Отправка файла как HTTP-ответ
    with open(file_path, 'rb') as file:
        response = HttpResponse(file, content_type=mime_type)
        response['Content-Disposition'] = f'attachment; filename="{backup_sahr_table()[1]}"'
        return response
    

def review_list(request):
    reviews = Review.objects.all()
    form = ReviewForm()

    if request.method == 'POST':
        print(request.POST)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.POST.get('user')
            review.save()
            messages.success(request, 'Спасибо за Ваш отзыв!')
            return redirect('review_list')  # Перенаправить на ту же страницу

    return render(request, 'review_list.html', {'reviews': reviews, 'form': form})




