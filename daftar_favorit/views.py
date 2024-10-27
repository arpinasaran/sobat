from django.shortcuts import render, redirect, get_object_or_404,reverse
from daftar_favorit.models import Favorite
from product.models import DrugEntry
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
# def show_json(request):
#     data = MoodEntry.objects.filter(user=request.user)
#     return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def show_favorite(request):
    favorite_item = Favorite.objects.filter(user=request.user)
    # print(User)
    context = {
        
        'favorite_items':favorite_item
    }
    return render(request,'favorite.html',context)

def show_json(request):
    data = Favorite.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def show_json_by_id(request, id):
    data = Favorite.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
@login_required
def add_to_favorites(request, product_id):
    # Dapatkan produk berdasarkan ID, atau berikan 404 jika tidak ditemukan
       
    product = get_object_or_404(DrugEntry, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    
    # Redirect to a valid URL
    if created:
       return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed', 'message': 'Invalid request'}, status=400)


@login_required
def remove_from_favorites(request, product_id):
    product = get_object_or_404(Favorite, pk=product_id)
    context = {
        'favorite': product
    }
    if request.method == 'POST':    
        product.delete()
        # messages.success(request, 'Favorit berhasil dihapus.')
        return redirect('daftar_favorite:show_favorite')
    
    return render(request, 'delete_favorite.html', context)

@login_required
def get_favorite_count(request):
    favorite_count = Favorite.objects.filter(user=request.user).count()
 
   
    
    return JsonResponse({'favorite_count': favorite_count})