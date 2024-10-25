from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import ShopProfile, Product
from .forms import ShopProfileForm, ProductForm

def shop_profile(request, shop_id):
    shop = get_object_or_404(ShopProfile, id=shop_id)
    products = shop.products.all().order_by('?')  # Random order for beranda
    categories = Product.objects.filter(shop=shop).values_list('category', flat=True).distinct()
    
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
    
    categories = Product.objects.filter(shop=shop).values_list('category', flat=True).distinct()
    
    context = {
        'shop': shop,
        'products': products,
        'categories': categories,
        'current_category': category,
        'is_owner': request.user == shop.owner if request.user.is_authenticated else False
    }
    return render(request, 'shop/catalog.html', context)

def shop_list(request):
    shops = ShopProfile.objects.all().order_by('-created_at')
    return render(request, 'shop/shop_list.html', {'shops': shops})


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
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.shop = shop
            product.save()
            messages.success(request, 'Product added successfully.')
            return redirect('shop:profile', shop_id=shop_id)
    else:
        form = ProductForm()
    
    return render(request, 'shop/add_product.html', {'form': form, 'shop': shop})