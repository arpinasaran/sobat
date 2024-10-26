#views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from .models import ShopProfile, ShopProduct
from .forms import ShopProfileForm, ShopProductForm

def shop_list(request):
    shops = ShopProfile.objects.all().order_by('-created_at')
    return render(request, 'shop/shop_list.html', {'shops': shops})

def shop_profile(request, shop_id):
    shop = get_object_or_404(ShopProfile, id=shop_id)
    products = shop.products.all().order_by('?')  # Random order for beranda
    categories = ShopProduct.objects.filter(shop=shop).values_list('category', flat=True).distinct()
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
    if category and category != 'all':
        products = products.filter(category=category)
    categories = ShopProduct.objects.filter(shop=shop).values_list('category', flat=True).distinct()
    context = {
        'shop': shop,
        'products': products,
        'categories': categories,
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
def add_product(request, shop_id):
    shop = get_object_or_404(ShopProfile, id=shop_id)
    if request.user != shop.owner:
        messages.error(request, "You don't have permission to add products to this shop.")
        return redirect('shop:profile', shop_id=shop_id)
    
    if request.method == 'POST':
        form = ShopProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.shop = shop
            product.save()
            messages.success(request, 'Product added successfully.')
            return redirect('shop:profile', shop_id=shop_id)
    else:
        form = ShopProductForm()
    return render(request, 'shop/add_product.html', {'form': form, 'shop': shop})

@login_required
def edit_product(request, shop_id, product_id):
    shop = get_object_or_404(ShopProfile, id=shop_id)
    product = get_object_or_404(ShopProduct, id=product_id, shop=shop)
    
    if request.user != shop.owner:
        raise PermissionDenied("You don't have permission to edit this product")
    
    if request.method == 'POST':
        form = ShopProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('shop:profile', shop_id=shop_id)
    else:
        form = ShopProductForm(instance=product)
    
    return render(request, 'shop/edit_product.html', {
        'form': form,
        'shop': shop,
        'product': product
    })

@login_required
def delete_product(request, shop_id, product_id):
    shop = get_object_or_404(ShopProfile, id=shop_id)
    product = get_object_or_404(ShopProduct, id=product_id, shop=shop)
    
    if request.user != shop.owner:
        return HttpResponseForbidden("You don't have permission to delete this product")
    
    if request.method == 'GET':
        return render(request, 'shop/delete_product.html', {
            'shop': shop,
            'product': product
        })
    
    if request.method == 'POST':
        product.delete()
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