# urls.py

from django.urls import path
from . import views
app_name = 'daftar_favorit' 
urlpatterns = [
    path('', views.show_favorite, name='show_favorite'),
    path('add', views.add_to_favorite, name='add_to_favorite'),
    path('remove_from_favorite/<uuid:product_id>', views.remove_from_favorites, name='remove_from_favorite'),
]
