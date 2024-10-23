from django.urls import path, include
from shop.views import show_main

app_name = 'shop'

urlpatterns = [
    path('', show_main, name='show_main'),
]