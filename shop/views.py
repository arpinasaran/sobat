#views.py
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from .models import ShopProfile, ShopProduct
from .forms import ShopProfileForm, ManageProductForm
from product.models import DrugEntry
from collections import defaultdict

from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt

import base64
from django.core.files.base import ContentFile
from datetime import datetime
from django.conf import settings

def shop_list(request):
    shops = ShopProfile.objects.all().order_by('-created_at')
    return render(request, 'shop/shop_list.html', {'shops': shops})

def shop_profile(request, shop_id):
    shop = get_object_or_404(ShopProfile, id=shop_id)
    products = shop.products.all().order_by('?')  # Random order for beranda
    
    # Get categories through the related DrugEntry model
    categories = DrugEntry.objects.filter(
        shop_products__shop=shop  # Changed from shopproduct__shop to shop_products__shop
    ).values_list('category', flat=True).distinct()
    
    context = {
        'shop': shop,
        'products': products,
        'categories': categories,
        'is_owner': request.user == shop.owner if request.user.is_authenticated else False
    }
    return render(request, 'shop/profile.html', context)

def shop_catalog(request, shop_id, category=None):
    shop = get_object_or_404(ShopProfile, id=shop_id)
    products = shop.products.all()

    # Filter by category if specified
    if category and category != 'all':
        products = products.filter(category=category)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    # Retrieve distinct categories
    categories = DrugEntry.objects.filter(
        shop_products__shop=shop
    ).values_list('category', flat=True).distinct()

    context = {
        'shop': shop,
        'products': products,
        'categories': sorted(set(categories)),
        'current_category': category,
        'is_owner': request.user == shop.owner if request.user.is_authenticated else False
    }
    return render(request, 'shop/catalog.html', context)

@login_required
def create_shop(request):
    if request.user.role != 'apoteker':
        raise PermissionDenied("Only apoteker can create shops")
    
    if request.method == 'POST':
        form = ShopProfileForm(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.owner = request.user
            shop.save()
            messages.success(request, 'Shop created successfully.')
            return redirect('shop:list')
    else:
        form = ShopProfileForm()
    
    return render(request, 'shop/create_shop.html', {'form': form})

@login_required
def edit_profile(request, shop_id):
    shop = get_object_or_404(ShopProfile, id=shop_id)
    if request.user != shop.owner:
        messages.error(request, "You don't have permission to edit this shop.")
        return redirect('shop:profile', shop_id=shop_id)
    
    if request.method == 'POST':
        form = ShopProfileForm(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            form.save()
            messages.success(request, 'Shop profile updated successfully.')
            return redirect('shop:profile', shop_id=shop_id)
    else:
        form = ShopProfileForm(instance=shop)
    return render(request, 'shop/edit_profile.html', {'form': form, 'shop': shop})

@login_required
def manage_products(request, shop_id):
    shop = get_object_or_404(ShopProfile, id=shop_id)
    
    if request.user != shop.owner:
        messages.error(request, "You don't have permission to manage products in this shop.")
        return redirect('shop:profile', shop_id=shop_id)
    
    if request.method == 'POST':
        form = ManageProductForm(request.POST, shop=shop)
        if form.is_valid():
            selected_products = form.cleaned_data['selected_products']
            
            # Get current products in shop
            current_products = set(ShopProduct.objects.filter(shop=shop).values_list('product_id', flat=True))
            # Convert selected products to set of IDs
            new_products = set(product.id for product in selected_products)
            
            # Remove products that were unselected
            products_to_remove = current_products - new_products
            ShopProduct.objects.filter(shop=shop, product_id__in=products_to_remove).delete()
            
            # Add newly selected products
            products_to_add = new_products - current_products
            for product_id in products_to_add:
                ShopProduct.objects.create(
                    shop=shop,
                    product_id=product_id,
                )
            
            messages.success(request, 'Shop products updated successfully.')
            return redirect('shop:profile', shop_id=shop_id)
    else:
        form = ManageProductForm(shop=shop)

    # Annotate each product with 'is_selected' based on current shop products
    products = DrugEntry.objects.all()
    for product in products:
        product.is_selected = ShopProduct.objects.filter(shop=shop, product_id=product.id).exists()
    
    context = {
        'form': form,
        'shop': shop,
        'products': products
    }
    return render(request, 'shop/manage_products.html', context)

@login_required
def delete_product(request, shop_id, product_id):
    shop = get_object_or_404(ShopProfile, id=shop_id)
    shop_product = get_object_or_404(ShopProduct, shop=shop, product_id=product_id)
    
    if request.user != shop.owner:
        messages.error(request, "You don't have permission to delete products from this shop.")
        return redirect('shop:profile', shop_id=shop_id)
    
    shop_product.delete()
    messages.success(request, 'Product removed from shop successfully.')
    return redirect('shop:profile', shop_id=shop_id)

@login_required
def delete_shop(request, shop_id):
    shop = get_object_or_404(ShopProfile, id=shop_id)
    
    if request.user != shop.owner:
        return HttpResponseForbidden("You don't have permission to delete this shop")
    
    if request.method == 'GET':
        return render(request, 'shop/delete_shop.html', {'shop': shop})
    
    if request.method == 'POST':
        shop.delete()
        return redirect('shop:list')

@csrf_exempt
def show_json(request):
    try:
        shops = ShopProfile.objects.all()
        data = json.loads(serializers.serialize("json", shops))
        
        # Add full URL to profile images
        for item in data:
            if item['fields']['profile_image']:
                item['fields']['profile_image'] = request.build_absolute_uri(
                    settings.MEDIA_URL + item['fields']['profile_image']
                )
        
        # Create response with the modified data
        response = JsonResponse(data, safe=False)
        
        # Add CORS headers
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        
        return response
    except Exception as e:
        print(f"Error in show_json: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)
    
def show_json_by_id(request, id):
    try:
        shop = get_object_or_404(ShopProfile, id=id)
        return HttpResponse(serializers.serialize("json", [shop]), 
                          content_type="application/json")
    except (ValueError, TypeError):
        return JsonResponse({
            "error": "Invalid shop ID format"
        }, status=400)
    
@csrf_exempt
@login_required
def create_shop_flutter(request):
    if request.method == 'POST':
        try:
            # Validasi apakah user adalah apoteker
            if not request.user.groups.filter(name='Apoteker').exists():
                return JsonResponse({
                    "status": "error",
                    "message": "Only apoteker can add a shop."
                }, status=403)

            # Ambil data dari request
            name = request.POST.get('name', 'Unnamed Shop')
            address = request.POST.get('address', 'No Address Provided')
            opening_time = request.POST.get('opening_time', '00:00')
            closing_time = request.POST.get('closing_time', '23:59')

            # Validasi waktu
            def validate_time_format(time_str):
                try:
                    datetime.strptime(time_str, '%H:%M')
                    return time_str
                except ValueError:
                    raise ValueError("Invalid time format. Use HH:MM.")

            opening_time = validate_time_format(opening_time)
            closing_time = validate_time_format(closing_time)

            # Buat toko baru
            new_shop = ShopProfile.objects.create(
                name=name,
                address=address,
                opening_time=opening_time,
                closing_time=closing_time,
                owner=request.user,  # owner otomatis dari user login
            )

            return JsonResponse({
                "status": "success",
                "data": {
                    "name": new_shop.name,
                    "address": new_shop.address,
                    "opening_time": str(new_shop.opening_time),
                    "closing_time": str(new_shop.closing_time),
                }
            }, status=201)

        except ValueError as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            }, status=500)

@login_required
def get_user_role(request):
    return JsonResponse({
        'role': 'apoteker' if request.user.groups.filter(name='Apoteker').exists() else 'user'
    })