import re
from django.shortcuts import redirect
import redis
from finder.forms import InputValue
from finder.models import Remains
from django.db.models import Q, Sum



def clear_sort(request):
    request.session['project'] = ''
    return redirect("main")


def choice_project_dict(request):  # Словарь из выбранных проектов
    all_project = Remains.objects.values_list("project", flat=True).distinct()  # переводит из картежа в список уникальные значения
    projects = request.POST.getlist("data_project")  # Выбор пользователя
    request.session['project'] = projects

    for i, projects in enumerate(projects):
        request.session['i'] = projects
    
    return {"all_project": all_project, "project": request.session.get('projects')}


def get_context_input_filter_all(request):  # Поиск всему
    form = InputValue(request.POST)
    metiz_all = Q()  # Создаем пустой объект Q
    comment_filter = Q()
    repl_a = Q()
    query = Q()
    fi = Q()
    if request.method == "POST":
        input_str = str(request.POST["input"])

        if input_str.startswith("*"):  # поиск по коду
            query = Q(code__startswith=input_str[1:])
            error_message = "Такой код не найден"

        elif input_str.startswith("-"):  # поиск по коментарию
            values = input_str[1:].split(" ")  # сбор значений с инпута по комменту
            for v in values:
                query &= Q(comment__icontains=v)
            error_message = "Такой коментарий не найден"

        elif input_str != "":  # метизы и текст
            values = input_str.split(" ")  # сбор значений с инпута
            for v in values:
                
                if re.match(r"^(\d+(\.\d+)?[*]\d+|5f[*]\d+)$", v):
                    v1 = v.lower().replace("*", "х")  # Кириллица
                    v2 = v.lower().replace("*", "x")  # Латиница
                    metiz_all = (
                        Q(title__icontains=v1)
                        | Q(title__icontains=v2)
                        | Q(title__icontains=v))
                    
                elif re.match(r"^[aа][24]\b", v):
                    r1 = v.lower().replace('а', 'a') #Меняем кирилицу на латиницу A4, A2
                    repl_a = (Q(title__icontains=v) | Q(title__icontains=r1))
                    
                elif v.startswith('-'):
                    fi = Q(comment__icontains=v[1:])  
                    
                else:
                    query &= Q(title__icontains=v)
        query_all = query & metiz_all & repl_a & fi   
        error_message = "Товар не найден"
        
        if not request.session.get('project'):
            request.session['project'] = ''
        projects_filter_q = Q()
        for value in request.session.get('project'):
            projects_filter_q |= Q(
                **{"project": value})  # Динамическое создание Q по выбранным проектам

        remains = (
            Remains.objects.filter(projects_filter_q)
            .filter(query_all)
            .filter(comment_filter)[:500] | Remains.objects.filter(article__contains=input_str)[:500])
        if (not remains.exists()):  # если ничего не найдено из нескольких значений в инпуте
            return {
                "form": form,
                "e_art_title": error_message,
            }
        return {
            "remains": remains,
            "form": form,
            "project": request.session.get('project'),
        }
    else:
        return {
            "form": form,
            "project": request.session.get('project'),
        }  # Возврат контест GET
        
        
        
  
