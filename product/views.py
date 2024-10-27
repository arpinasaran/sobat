from django.shortcuts import render, redirect, reverse
from product.forms import DrugEntryForm
from product.models import DrugEntry
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from daftar_favorit.models import Favorite

@login_required(login_url='/login')
def show_main(request):
    products = DrugEntry.objects.all()
    return render(request, "all_products.html", {'products': products})

def create_drug(request):
    if request.method == 'POST':
        form = DrugEntryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product:show_main')  
    else:
        form = DrugEntryForm()
    
    context = {'form': form}
    return render(request, "create_drug.html", context)

@csrf_exempt
@require_POST
def create_drug_ajax(request):
    # Mendapatkan data dari permintaan POST
    name = request.POST.get("name")
    desc = request.POST.get("desc")
    category = request.POST.get("category")
    drug_type = request.POST.get("drug_type")
    drug_form = request.POST.get("drug_form")
    price = request.POST.get("price")
    availibility = request.POST.get("availibility") == "true"  # Mengonversi string ke boolean
    image = request.FILES.get("image")  # Mengambil gambar dari FILES, bukan POST

    # Membuat entri baru dalam model DrugEntry
    new_drug = DrugEntry(
        name=name,
        desc=desc,
        category=category,
        drug_type=drug_type,
        drug_form=drug_form,
        price=int(price),
        availibility=availibility,
        image=image
    )
    new_drug.save()

    return HttpResponse(b"CREATED", status=201)

@csrf_exempt
@require_POST
def edit_drug_ajax(request, id):
    # Mendapatkan entri berdasarkan ID
    drug = DrugEntry.objects.get(pk=id)
    
    # Mengambil data dari request POST
    drug.name = request.POST.get("name", drug.name)
    drug.desc = request.POST.get("desc", drug.desc)
    drug.category = request.POST.get("category", drug.category)
    drug.drug_type = request.POST.get("drug_type", drug.drug_type)
    drug.drug_form = request.POST.get("drug_form", drug.drug_form)
    drug.price = int(request.POST.get("price", drug.price))
    drug.availibility = request.POST.get("availibility") == "true"
    
    # Mengambil file gambar baru jika ada, atau mempertahankan gambar lama
    if 'image' in request.FILES:
        drug.image = request.FILES['image']
    
    # Menyimpan perubahan
    drug.save()

    return HttpResponse(b"UPDATED", status=200)

def edit_drug(request, id):
    product = DrugEntry.objects.get(pk=id)

    form = DrugEntryForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('product:show_main'))

    context = {'form': form}
    return render(request, "create_drug.html", context) #still need to fix

def delete_drug(request, id):
    product = DrugEntry.objects.get(pk=id)

    product.delete()

    return HttpResponseRedirect(reverse('product:show_main'))

def show_drug(request, id):
    product = DrugEntry.objects.get(pk=id)

    return render(request, "product_detail.html", {'product': product})

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
