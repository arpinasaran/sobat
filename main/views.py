from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from product.models import DrugEntry

# Create your views here.

@login_required(login_url='/login')
def show_main(request):
    last_login = request.COOKIES.get('last_login', None)

    context = {
        'name': request.user.username,
        'last_login': last_login
    }

    return render(request, "main.html", context)

def product_list(request):
    products = DrugEntry.objects.all()  # Ambil semua produk dari database
    return render(request, 'main.html', {'products': products})