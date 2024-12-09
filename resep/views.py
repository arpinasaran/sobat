from django.shortcuts import render
from resep.models import Resep
from product.models import DrugEntry as Produk
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
def show_resep(request):
    resep = Resep.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.amount for item in resep)

    context = {
        'user': request.user,
        'resep': resep,
        'total_price': total_price
    }

    return render(request, "resep.html", context)

@require_POST
@login_required
def update_amount(request):
    deleted = False
    reloaded = False

    resep_id = request.POST.get('resep_id')
    action = request.POST.get('action')

    resep = get_object_or_404(Resep, id=resep_id, user=request.user)
    
    if action == 'increase' and resep.amount < 99:
        resep.amount += 1
        resep.save()
        deleted = False
    elif action == 'decrease':
        if resep.amount > 1:
            resep.amount -= 1
            resep.save()
            deleted = False
        else:
            resep.delete()
            deleted = True
            reloaded = not Resep.objects.filter(user=request.user).exists()

    # Hitung total harga baru setelah update
    total_price = sum(item.product.price * item.amount for item in Resep.objects.filter(user=request.user))

    return JsonResponse({
        'amount': resep.amount if not deleted else 0,  # Kirim jumlah 0 jika produk dihapus
        'total_price': float(total_price),
        'deleted': deleted,  # Flag untuk menandakan produk terhapus
        'reloaded' : reloaded
    })

@login_required
def add_to_resep(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Produk, id=product_id)

        # Menambahkan produk ke resep atau memperbarui jumlah jika sudah ada
        resep, created = Resep.objects.get_or_create(user=request.user, product=product)

        if not created and resep.amount < 99:
            resep.amount += 1
        else:
            resep.amount = 1

        resep.save()

        return JsonResponse({'status': 'success', 'amount': resep.amount})
    return JsonResponse({'status': 'failed', 'message': 'Invalid request'}, status=400)

from django.views.decorators.csrf import csrf_exempt

@login_required
def clear_recipes(request):
    if request.method == 'POST':
        # Logika untuk menghapus semua resep
        Resep.objects.filter(user=request.user).delete()
        return JsonResponse({'success': True})

def show_json(request):
    data = Resep.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = Resep.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
