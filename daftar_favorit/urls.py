# urls.py

from django.urls import path
from . import views
from django.urls import path, include
app_name = 'daftar_favorite' 
urlpatterns = [
    path('', views.show_favorite, name='show_favorite'),
    path('add/<uuid:product_id>/', views.add_to_favorites, name='add_to_favorite'),
    path('delete/<uuid:product_id>/', views.delete_favorite, name='delete_favorite'),
    path('json/', views.show_json, name='show_json'),
    path('', include('main.urls')),
    path('api/favorite_count/', views.get_favorite_count, name='get_favorite_count'),
    path('get-count/', views.get_favorite_count, name='get_favorite_count'),
    path('check-status/<uuid:product_id>/', views.check_favorite_status, name='check_favorite_status'),
]
