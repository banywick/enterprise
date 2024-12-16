from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from comersant.forms import FilterForm, InputDataForm, InvoiceEditForm, InvoiceEditFormStatus, AddSupplerForm
from comersant.models import Invoice, Leading, Supler, DescriptionProblem
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib.auth.decorators import login_required



def add_session_filter(request):
    if request.method == 'POST':
        supplier_id = request.POST.get('supplier')
        leading_id = request.POST.get('leading')
        if supplier_id:
            try:
                supplier = Supler.objects.get(id=supplier_id)
                request.session['supplier_name'] = supplier.name
            except ObjectDoesNotExist:
                request.session['supplier_name'] = None
        else:
            request.session['supplier_name'] = None
        if leading_id:
            try:
                leading = Leading.objects.get(id=leading_id)
                request.session['leading_name'] = leading.name
            except ObjectDoesNotExist:
                request.session['leading_name'] = None
        else:
            request.session['leading_name'] = None
        return redirect('shortfalls')
    return redirect('shortfalls')

@login_required
def clear_filter(request):
    request.session['leading_name'] = None
    request.session['supplier_name'] = None
    return redirect('shortfalls')



@login_required
def add_suppler(request):
    if request.method == 'POST':
        form = AddSupplerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shortfalls')    
        return redirect('shortfalls')    

@login_required
def shortfalls_view(request):
    form = InputDataForm()
    filter_form = FilterForm(request.POST)
    add_suppler = AddSupplerForm()
    # Получаем значения из сессии
    supplier_name = request.session.get('supplier_name')
    leading_name = request.session.get('leading_name')
    filters = {'supplier_name': supplier_name, 'leading_name': leading_name }
    # Создаем Q-объекты для фильтрации
    q_objects = Q()
    if supplier_name:
        q_objects &= Q(supplier__name=supplier_name)

    if leading_name:
        q_objects &= Q(leading__name=leading_name)
    # Фильтруем кверисет на основе Q-объектов
    invoices = Invoice.objects.filter(q_objects).order_by("id")
    for invoice in invoices:
        if invoice.quantity.is_integer():
            invoice.quantity = int(invoice.quantity)
    context = {
        'form': form,
        'filter_form': filter_form,
        'invoices': invoices,
        'add_suppler': add_suppler,
        'filters': filters
    }
    return render(request, 'comersant/comers.html', context)

@login_required
def input_data(request):
    if request.method == 'POST':
        form = InputDataForm(request.POST)
        if form.is_valid():
            description_problem_name = form.cleaned_data['description_problem']

            # Попытаемся получить существующий объект DescriptionProblem
            description_problem, created = DescriptionProblem.objects.get_or_create(name=description_problem_name)
            invoice = Invoice(
                invoice_number=form.cleaned_data['invoice'],
                date=form.cleaned_data['date'],
                supplier=form.cleaned_data['supplier'],
                article=form.cleaned_data['hidden_article'],
                name=form.cleaned_data['auto_title'],
                unit=form.cleaned_data['hidden_unit'],  # Пример значения, можно изменить
                quantity=form.cleaned_data['quantity'],
                comment=form.cleaned_data['comment'],
                description_problem=description_problem,
                specialist=form.cleaned_data['specialist'],
                leading=form.cleaned_data['leading']
            )
            invoice.save()
            print(form.cleaned_data)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = InputDataForm()

    return redirect('shortfalls')     

@login_required       
def edit_row_form(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    if request.method == "POST":
        form = InvoiceEditForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            return redirect('shortfalls') 
    else:
        form = InvoiceEditForm(instance=invoice)
    return render(request, 'comersant/comers.html', {'form': form, 'flag': 'row'})

@login_required    
def edit_status(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    if request.method == "POST":
        form = InvoiceEditFormStatus(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            return redirect('shortfalls') 
    else:
        form = InvoiceEditFormStatus(instance=invoice)
    return render(request, 'comersant/comers.html', {'form': form, 'flag': 'status'})

    
@login_required
def delete_row(request, id):
    get_object_or_404(Invoice, id=id).delete()
    return redirect('shortfalls') 


