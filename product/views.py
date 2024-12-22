from django.shortcuts import render, redirect, reverse
from product.forms import DrugEntryForm
from product.models import DrugEntry
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from daftar_favorit.models import Favorite
from shop.models import ShopProfile

@login_required(login_url='/login')
def show_main(request):
    products = DrugEntry.objects.all()
    return render(request, "all_products.html", {'products': products})

# def create_drug(request):
#     if request.method == 'POST':
#         form = DrugEntryForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('product:show_main')  
#     else:
#         form = DrugEntryForm()
    
#     context = {'form': form}
#     return render(request, "create_drug.html", context)

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
    image = request.FILES.get("image")  # Mengambil gambar dari FILES, bukan POST

    # Membuat entri baru dalam model DrugEntry
    new_drug = DrugEntry(
        name=name,
        desc=desc,
        category=category,
        drug_type=drug_type,
        drug_form=drug_form,
        price=int(price),
        image=image
    )
    new_drug.save()

    return HttpResponse(b"CREATED", status=201)

@csrf_exempt
def create_drug_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_drug = DrugEntry.objects.create(
            name=data["name"],
            desc=data["desc"],
            category=data["category"],
            drug_type=data["drug_type"],
            drug_form=data["drug_form"],
            price=int(data["price"]),
            image=["image"]
        )
        new_drug.save()
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

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
    
    # Mengambil file gambar baru jika ada, atau mempertahankan gambar lama
    if 'image' in request.FILES:
        drug.image = request.FILES['image']
    
    # Menyimpan perubahan
    drug.save()

    return HttpResponse(b"UPDATED", status=200)

# def edit_drug(request, id):
#     product = DrugEntry.objects.get(pk=id)

#     form = DrugEntryForm(request.POST or None, instance=product)

#     if form.is_valid() and request.method == "POST":
#         form.save()
#         return HttpResponseRedirect(reverse('product:show_main'))

#     context = {'form': form}
#     return render(request, "create_drug.html", context) #still need to fix

def delete_drug(request, id):
    product = DrugEntry.objects.get(pk=id)

    product.delete()

    return HttpResponseRedirect(reverse('product:show_main'))

def show_drug(request, id):
    product = DrugEntry.objects.get(pk=id)

    return render(request, "product_detail.html", {'product': product})

def show_seller(request, id):
    product = DrugEntry.objects.get(pk=id)

    return render(request, 'show_seller.html', {'product' : product})

def show_json(request):
    data = DrugEntry.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = DrugEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

from django.http import HttpResponse
from product.models import DrugEntry
from shop.models import ShopProfile, ShopProduct

def update(request):
    # Step 1: Iterate through all ShopProduct entries
    all_shop_products = ShopProduct.objects.all()

    for shop_product in all_shop_products:
        # Get the related shop and product from each ShopProduct entry
        shop = shop_product.shop
        product = shop_product.product

        # Step 2: Check if the shop is already associated with the product
        if not product.shops.filter(id=shop.id).exists():
            # If not, add the shop to the product's shops
            product.shops.add(shop)

    return HttpResponse("Updated all shop-product relationships successfully.")

