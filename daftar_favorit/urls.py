# urls.py

from django.urls import path
from . import views
app_name = 'daftar_favorite' 
urlpatterns = [
    path('', views.show_favorite, name='show_favorite'),
    path('add/<uuid:product_id>', views.add_to_favorite, name='add_to_favorite'),
    path('delete/<uuid:product_id>', views.remove_from_favorites, name='delete_favorite'),
    path('json/', views.show_json, name='show_json'),
]
