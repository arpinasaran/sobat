from django.urls import path
from main.views import show_main,product_list
from django.urls import path, include

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('', product_list, name='main_page'),
    # path('favorite/', include('daftar_favorit.urls')),  # Ini menghubungkan URL dari aplikasi `favorite`

]