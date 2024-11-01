from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import json
from comersant.form import InputDataForm, InvoiceEditForm, InvoiceEditFormStatus
from comersant.models import Invoice

def shortfalls_view(request):
    form = InputDataForm()
    invoices = Invoice.objects.all()  # Получаем все объекты модели Invoice
    context = {
        'form': form,
        'invoices': invoices
    }
    return render(request, 'comersant/comers.html', context)

def input_data(request):
    if request.method == 'POST':
        form = InputDataForm(request.POST)
        if form.is_valid():
            invoice = Invoice(
                invoice_number=form.cleaned_data['invoice'],
                date=form.cleaned_data['date'],
                supplier=form.cleaned_data['supplier'],
                article=form.cleaned_data['hidden_article'],
                name=form.cleaned_data['auto_title'],
                unit=form.cleaned_data['hidden_unit'],  # Пример значения, можно изменить
                quantity=form.cleaned_data['quantity'],
                comment=form.cleaned_data['comment'],
                specialist=form.cleaned_data['specialist'],
                leading=form.cleaned_data['leading']
            )
            invoice.save()
            return redirect('shortfalls')
        
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

    

def delete_row(request, id):
    get_object_or_404(Invoice, id=id).delete()
    return redirect('shortfalls') 


