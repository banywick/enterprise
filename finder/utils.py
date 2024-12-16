import re
from django.shortcuts import redirect
import redis
from finder.forms import InputValue
from finder.models import Remains
from django.db.models import Q
from finder.standarts import standarts_collection
from collections import Counter


def connect_redis():
    return redis.StrictRedis(host="localhost", port=6379, db=0)

def clear_sort(request):
    request.session["project"] = ""
    return redirect("main")


def choice_project_dict(request):
    # Словарь из выбранных проектов
    all_project = Remains.objects.values_list("project", flat=True).distinct()  # переводит из картежа в список уникальные значения
    projects = request.POST.getlist("data_project")  # Выбор пользователя

    # Сохраняем выбор пользователя в сессии
    request.session["project"] = projects

    # Инициализируем список выборов проектов, если он еще не существует
    if "project_choices" not in request.session:
        request.session["project_choices"] = []

    # Добавляем текущие выборы в список выборов проектов
    request.session["project_choices"].extend(projects)

    # Явно указываем, что сессия была изменена
    request.session.modified = True

    # Убедимся, что все элементы в project_choices являются строками
    project_choices = request.session["project_choices"]
    if any(isinstance(item, list) for item in project_choices):
        # Если есть списки, преобразуем их в строки
        project_choices = [item if isinstance(item, str) else ''.join(item) for item in project_choices]
        request.session["project_choices"] = project_choices

    # Подсчитываем количество выборов каждого проекта
    project_counter = Counter(project_choices)

    # Получаем 5 самых часто выбранных проектов
    most_common_projects = project_counter.most_common(4)

    # Преобразуем результат в список проектов
    top_projects = [project for project, count in most_common_projects]

    return {
        "all_project": all_project,
        "project": request.session.get("project"),
        "top_projects": top_projects
    }

def get_context_input_filter_all(request):  # Поиск всему
    form = InputValue(request.POST)
    if request.method == "POST":
        input_str = str(request.POST["input"])
        values = input_str.split(" ")  # сбор значений с инпута

        def search_standarts():
            query_standart_list = Q()
            replace_a = Q()
            metiz_all = Q()
            if (
                input_str.startswith("+") and len(values) >= 2
            ):  # Список совпадения из инпут
                for standart_list in standarts_collection():
                    if values[1] in standart_list:
                        for item in standart_list:
                            query_standart_list |= Q(title__icontains=item)
                if not query_standart_list:
                    query_standart_list = Q()
                for element in values:
                    if re.match(r"^(\d+(\.\d+)?[*]\d+|5f[*]\d+)$", element):
                        v1: str = element.lower().replace("*", "х")  # Кириллица
                        v2 = element.lower().replace("*", "x")  # Латиница
                        metiz_all = (
                            Q(title__icontains=v1)
                            | Q(title__icontains=v2)
                            | Q(title__icontains=element)
                        )
                    if re.match(r"^[aа][24]\b", element):
                        vriant1 = element.lower().replace(
                            "а", "a"
                        )  # Меняем кирилицу на латиницу A4, A2
                        replace_a = Q(title__icontains=element) | Q(
                            title__icontains=vriant1
                        )
                return (
                    Q(title__icontains=values[0][1:])
                    & query_standart_list
                    & metiz_all
                    & replace_a
                )
            else:
                return Q()

        def search_code():
            if input_str.startswith("*"):  # поиск по коду
                return Q(code__startswith=input_str[1:])
            else:
                return Q()

        def search_start_comment():
            comments = Q()
            if input_str.startswith("-"):  # поиск по коментарию
                values[0] = values[0][1:]
                for comment in values:
                    comments &= Q(comment__icontains=comment)
                return comments
            else:
                return Q()
        
        def search_another():

            metiz_all = Q()
            any_elements = Q()
            replace_a = Q()
            comment_body = Q()
            if input_str and input_str[0] not in ("+", "*", "-"):
                for element in values:
                    if re.match(r"^(\d+(\.\d+)?[*]\d+|5f[*]\d+)$", element):
                        v1: str = element.lower().replace("*", "х")  # Кириллица
                        v2 = element.lower().replace("*", "x")  # Латиница
                        metiz_all = (
                            Q(title__icontains=v1)
                            | Q(title__icontains=v2)
                            | Q(title__icontains=element)
                        )
                    if re.match(r"^[aа][24]\b", element):
                        vriant1 = element.lower().replace(
                            "а", "a"
                        )  # Меняем кирилицу на латиницу A4, A2
                        replace_a = Q(title__icontains=element) | Q(
                            title__icontains=vriant1
                        )

                    if element.startswith("-"):
                        comment_body = Q(comment__icontains=element[1:])

                    if (
                        not re.match(r"^(\d+(\.\d+)?[*]\d+|5f[*]\d+)$", element)
                        and not re.match(r"^[aа][24]\b", element)
                        and not element.startswith("-")
                    ):
                        any_elements &= Q(title__icontains=element)

                res = any_elements & metiz_all & replace_a & comment_body
                return res
            return Q()

        error_message = "Товар не найден"

        if not request.session.get("project"):
            request.session["project"] = ""
        projects_filter_q = Q()
        for value in request.session.get("project"):
            projects_filter_q |= Q(
                **{"project": value}
            )  # Динамическое создание Q по выбранным проектам


        def standart_context_html():
            standart_list = []
            if input_str.startswith("+") and len(values) >= 2:  # Список совпадения из инпут
                for standart_list in standarts_collection():
                        if values[1] in standart_list:
                            break
                return standart_list       


        remains = Remains.objects.filter(projects_filter_q).filter(
            search_standarts()
            | search_another()
            | search_code()
            | search_start_comment())[:500] |  Remains.objects.filter(
            article__contains=input_str)[:500]

        if (not remains.exists()): 
            return {
               
                "form": form,
                "e_art_title": error_message,
            }
        return {
            "remains": remains,
            "standart_list": standart_context_html(),
            "form": form,
            "project": request.session.get("project"),
        }
    else:
        return {
            "form": form,
            "project": request.session.get("project"),
        }  # Возврат контест GET
