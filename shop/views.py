from django.shortcuts import render, redirect
from shop.models import ShopEntry
from django.http import HttpResponse
from django.core import serializers

def show_main(request):
    shop_entries = ShopEntry.objects.all()

    context = {
        'TOKO BUNDAR'
    }

    return render(request, "main.html", context)
