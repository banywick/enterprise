import re
from django.shortcuts import redirect
import redis
from finder.forms import InputValue
from finder.models import Remains
from django.db.models import Q, Sum

from finder.standarts import standarts_collection


def clear_sort(request):
    request.session["project"] = ""
    return redirect("main")


def choice_project_dict(request):  # Словарь из выбранных проектов
    all_project = Remains.objects.values_list(
        "project", flat=True
    ).distinct()  # переводит из картежа в список уникальные значения
    projects = request.POST.getlist("data_project")  # Выбор пользователя
    request.session["project"] = projects

    for i, projects in enumerate(projects):
        request.session["i"] = projects

    return {"all_project": all_project, "project": request.session.get("projects")}


def get_context_input_filter_all(request):  # Поиск всему
    form = InputValue(request.POST)
  
    if request.method == "POST":
        input_str = str(request.POST["input"])
        values = input_str.split(" ")  # сбор значений с инпута

        def search_standarts():
            query_standart_list = Q()
            if input_str.startswith("+") and len(values) >= 2:  # Список совпадения из инпут
                for standart_list in standarts_collection():
                    if values[1] in standart_list:
                        for item in standart_list:
                            query_standart_list |= Q(title__icontains=item)
                return Q(title__icontains=values[0][1:]) & query_standart_list
            else: return Q()

        def search_code():
            if input_str.startswith("*"):  # поиск по коду
                return Q(code__startswith=input_str[1:])
            else: return Q()

        def search_start_comment():
            comments = Q()
            if input_str.startswith("-"):  # поиск по коментарию
                values[0] = values[0][1:]
                for comment in values:
                    comments &= Q(comment__icontains=comment)
                return comments
            else: return Q()    

        def search_block_size():
            if input_str:  # Размеры метизов
                metiz_all = Q()
                for element in values:
                    if re.match(r"^(\d+(\.\d+)?[*]\d+|5f[*]\d+)$", element):
                        v1: str = element.lower().replace("*", "х")  # Кириллица
                        v2 = element.lower().replace("*", "x")  # Латиница
                        metiz_all = (
                            Q(title__icontains=v1)
                            | Q(title__icontains=v2)
                            | Q(title__icontains=element))
                        return metiz_all
                    else: return Q()

        def search_replace_a():
            if input_str:
                replace_a = Q()
                for element in values:            
                    if re.match(r"^[aа][24]\b", element):
                        vriant1 = element.lower().replace( "а", "a")  # Меняем кирилицу на латиницу A4, A2
                        replace_a = Q(title__icontains=element) | Q(title__icontains=vriant1)
                        return replace_a
                    else: return Q()

        def search_comment_body():  

            if input_str and input_str != search_start_comment():
                for element in values:   
                    if element.startswith("-"):
                        return Q(comment__icontains=element[1:])
                else: return Q()

        def search_another():
            x = Q()
            if input_str:
                for element in values:
                    x &=  Q(title_icontains=element)
                return x
            return Q()
        print(search_another())    


        error_message = "Товар не найден"

        if not request.session.get("project"):
            request.session["project"] = ""
        projects_filter_q = Q()
        for value in request.session.get("project"):
            projects_filter_q |= Q(
                **{"project": value}
            )  # Динамическое создание Q по выбранным проектам

        remains = (
            Remains.objects.filter(projects_filter_q)
            .filter(search_code() | search_standarts())
            .filter(search_start_comment())[:100]
            | Remains.objects.filter(article__contains=input_str)[:50]
        )
        if (
            not remains.exists()
        ):  # если ничего не найдено из нескольких значений в инпуте
            return {
                "form": form,
                "e_art_title": error_message,
            }
        return {
            "remains": remains,
            "form": form,
            "project": request.session.get("project"),
        }
    else:
        return {
            "form": form,
            "project": request.session.get("project"),
        }  # Возврат контест GET
