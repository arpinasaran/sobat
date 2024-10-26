from django.shortcuts import render, redirect
from product.forms import DrugEntryForm
from product.models import DrugEntry
from django.http import HttpResponse
from django.core import serializers

def show_main(request):
    drug_entries = DrugEntry.objects.all()

    context = {
        'npm' : '2306123456',
        'name': 'Pak Bepe',
        'class': 'PBP E',
        'drug_entries' : drug_entries
    }

    return render(request, "main.html", context)

def create_drug_entry(request):
    form = DrugEntryForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('product:show_main')
    
    context = {'form': form}
    return render(request, "create_drug_entry.html", context)

def show_xml(request):
    data = DrugEntry.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = DrugEntry.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = DrugEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = DrugEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

