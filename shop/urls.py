# urls.py
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('shops/', views.shop_list, name='list'),
    path('shops/create/', views.create_shop, name='create_shop'),
    path('shops/<uuid:shop_id>/delete/', views.delete_shop, name='delete_shop'),
    path('<uuid:shop_id>/', views.shop_profile, name='profile'),
    path('<uuid:shop_id>/catalog/', views.shop_catalog, name='catalog'),
    path('<uuid:shop_id>/catalog/<str:category>/', views.shop_catalog, name='catalog_category'),
    path('<uuid:shop_id>/edit/', views.edit_profile, name='edit_profile'),
    path('<uuid:shop_id>/add-product/', views.add_product, name='add_product'),
    path('<uuid:shop_id>/product/<uuid:product_id>/edit/', views.edit_product, name='edit_product'),
    path('<uuid:shop_id>/product/<uuid:product_id>/delete/', views.delete_product, name='delete_product'),
] 