import json
from django.shortcuts import render, redirect, get_object_or_404,reverse
from daftar_favorit.forms import FavoriteForm
from daftar_favorit.models import Favorite
from product.models import DrugEntry
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse,HttpResponseNotFound
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




def show_json_by_id(request, id):
    data = Favorite.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(DrugEntry, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)

    if created:
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed'}, status=200)

@login_required
def delete_favorite(request, product_id):
    print(f"Trying to delete favorite with ID: {product_id}")  # Debugging line
    if request.method == 'POST':
        try:
            favorite_item = Favorite.objects.filter(id=product_id)
            favorite_item.delete()
            return JsonResponse({'status': 'success'})
        except Favorite.DoesNotExist:
            print("Item not found")  # Debugging line
            return HttpResponseNotFound('Item not found')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=200)

def get_favorite_count(request):
    favorite_count = Favorite.objects.filter(user=request.user).count()
 
   
    
    return JsonResponse({'favorite_count': favorite_count})
@login_required
def check_favorite_status(request, product_id):
    is_favorite = Favorite.objects.filter(
        user=request.user,
        product_id=product_id
    ).exists()
    
    return JsonResponse({
        'is_favorite': is_favorite
    })
    
    
def show_json(request):
    data = Favorite.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


@login_required
def edit_favorit(request, favorite_id):
    if request.method == "POST":
        # Ambil objek Favorite berdasarkan UUID
        favorite = get_object_or_404(Favorite, id=favorite_id, user=request.user)
        
        # Jika form menggunakan data JSON
        form = FavoriteForm(request.POST, instance=favorite)
        
        if form.is_valid():
            form.save()  # Simpan perubahan ke database
            return JsonResponse({"status": "success", "message": "Favorite updated successfully."}, status=200)
        else:
            return JsonResponse({"status": "error", "message": "Form is not valid.", "errors": form.errors}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Only POST requests are allowed."}, status=405)
