from django.contrib import admin
from .models import ShopProfile, Product

@admin.register(ShopProfile)
class ShopProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'opening_time', 'closing_time')
    search_fields = ('name', 'owner__username')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'category', 'price', 'is_available')
    list_filter = ('category', 'is_available', 'drug_type')
    search_fields = ('name', 'description', 'shop__name')