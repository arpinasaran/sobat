from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('<uuid:shop_id>/', views.shop_profile, name='profile'),
    path('shops/', views.shop_list, name='list'),
    path('<uuid:shop_id>/catalog/', views.shop_catalog, name='catalog'),
    path('<uuid:shop_id>/catalog/<str:category>/', views.shop_catalog, name='catalog_category'),
    path('<uuid:shop_id>/edit/', views.edit_profile, name='edit_profile'),
    path('<uuid:shop_id>/add-product/', views.add_product, name='add_product'),
]