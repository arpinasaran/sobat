from django.shortcuts import render, redirect, get_object_or_404,reverse
from .models import Favorite
from .models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse

# Create your views here.

@login_required
def show_favorite(request):
    favorite_item = Favorite.objects.filter(user=request.user   )
    context = {
        
        'favorite_items':favorite_item
    }
    return render(request,'favorite.html',context)

@login_required
def add_to_favorite(request, product_id):
    product = Favorite.objects.get(id=product_id)
    favorite_item, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, "Product added to Favorite")
    else:
        messages.info(request, "Product is already in your Favorite")
    return redirect('show_favorite')

@login_required
def remove_from_favorites(request, product_id):
    product = Favorite.objects.get(pk = product_id)
    product.delete()
    return HttpResponseRedirect(reverse('daftar_favorit:show_favorite'))