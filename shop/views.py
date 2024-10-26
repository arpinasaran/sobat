#views.py
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

    if category and category != 'all':
        products = products.filter(category=category)

    # Retrieve distinct categories from the related DrugEntry model
    categories = DrugEntry.objects.filter(
        shop_products__shop=shop
    ).values_list('category', flat=True).distinct()

    context = {
        'shop': shop,
        'products': products,
        'categories': sorted(set(categories)),  # Ensure categories are unique and sorted
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

# views.py
@login_required
def manage_products(request, shop_id):
    shop = get_object_or_404(ShopProfile, id=shop_id)
    
    if request.user != shop.owner:
        messages.error(request, "You don't have permission to manage products in this shop.")
        return redirect('shop:profile', shop_id=shop_id)
        
    if request.method == 'POST':
        selected_product_ids = request.POST.getlist('selected_products')
        
        # Get current products in shop
        current_products = set(ShopProduct.objects.filter(shop=shop).values_list('product_id', flat=True))
        
        # Keep selected product IDs as strings (assuming they are UUIDs)
        new_products = set(selected_product_ids)
        
        # Remove products that were unselected
        products_to_remove = current_products - new_products
        ShopProduct.objects.filter(shop=shop, product_id__in=products_to_remove).delete()
        
        # Add newly selected products
        products_to_add = new_products - current_products
        for product_id in products_to_add:
            ShopProduct.objects.create(
                shop=shop,
                product_id=product_id,
                is_available=True
            )

        messages.success(request, 'Shop products updated successfully.')
        return redirect('shop:profile', shop_id=shop_id)
    
    # Get all products and mark which ones are already in the shop
    all_products = DrugEntry.objects.all()
    selected_product_ids = set(ShopProduct.objects.filter(shop=shop).values_list('product_id', flat=True))
    
    # Add is_selected attribute to each product
    for product in all_products:
        product.is_selected = product.id in selected_product_ids
    
    context = {
        'shop': shop,
        'products': all_products
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

def product_detail(request, shop_id, product_id):
    shop = get_object_or_404(Shop, id=shop_id)
    product = get_object_or_404(Product, id=product_id)
    context = {
        'shop': shop,
        'product': product,
    }
    return render(request, 'shop/product_detail.html', context)
