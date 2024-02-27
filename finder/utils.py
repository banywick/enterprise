import re
from django.shortcuts import redirect
import redis
from finder.forms import InputValue
from finder.models import Remains
from django.db.models import Q, Sum


choice_project = dict()  # Хранилище выбранных проектов


def clear_sort(request):
    choice_project.clear()
    return redirect("main")


def choice_project_dict(request):  # Словарь из выбранных проектов
    all_project = Remains.objects.values_list(
        "project", flat=True
    ).distinct()  # переводит из картежа в список уникальные значения
    projects = request.POST.getlist("data_project")  # Выбор пользователя

    for i, project in enumerate(projects):
        choice_project[i] = project  # добавляем выбор в дикт
    return {"all_project": all_project, "project": choice_project.values()}


def get_context_input_filter_all(request):  # Поиск всему
    form = InputValue(request.POST)
    if request.method == "POST":
        input_str = str(request.POST["input"])
        if input_str.startswith("*"):  # поиск по коду
            query = Q(code__icontains=input_str[1:])
            error_message = "Такой код не найден"
        elif input_str.startswith("-"):  # поиск по коментарию
            values = input_str[1:].split(" ")  # сбор значений с инпута по комменту
            values += [""] * (
                4 - len(values)
            )  # Добавляем пустые строки, если введено менее четырех слов
            query = (
                Q(comment__icontains=values[0])
                & Q(comment__icontains=values[1])
                & Q(comment__icontains=values[2])
                & Q(comment__icontains=values[3])
            )
            error_message = "Такой коментарий не найден"
        else:
            values = input_str.split(" ")  # сбор значений с инпута
            values += [" "] * (5 - len(values))
            # )  # Добавляем пустые строки, если введено менее четырех слов
            metiz_all = Q()  # Создаем пустой объект Q
            any_text = []
            for v in values:
                if re.match(r"^(\d+(\.\d+)?[*]\d+|5f[*]\d+)$", v):
                    v1 = v.lower().replace("*", "х")  # Кириллица
                    v2 = v.lower().replace("*", "x")  # Латиница
                    metiz_all |= (
                        Q(title__icontains=v1)
                        | Q(title__icontains=v2)
                        | Q(title__icontains=v)
                    )
                else:
                    any_text.append(v)
            query = (
                Q(title__icontains=any_text[0])
                & Q(title__icontains=any_text[1])
                & Q(title__icontains=any_text[2])
                & Q(title__icontains=any_text[3])
            )
            error_message = "Товар не найден"
        projects_filter_q = Q()
        for value in choice_project.values():
            projects_filter_q |= Q(
                **{"project": value}
            )  # Динамическое создание Q по выбранным проектам
        remains = Remains.objects.filter(projects_filter_q).filter(
           query & metiz_all
        ) | Remains.objects.filter(article__contains=input_str)
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
            "project": choice_project.values(),
        }
    else:
        return {
            "form": form,
            "project": choice_project.values(),
        }  # Возврат контест GET
