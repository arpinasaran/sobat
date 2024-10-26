from django.contrib import admin
from .models import ShopProfile, ShopProduct

@admin.register(ShopProfile)
class ShopProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'opening_time', 'closing_time')
    search_fields = ('name', 'owner__username')

@admin.register(ShopProduct)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'shop', 'product_category', 'product_price', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('product__name', 'product__description', 'shop__name')
    
    # Custom methods to access fields from the related DrugEntry model
    def product_name(self, obj):
        return obj.product.name
    product_name.short_description = 'Product Name'
    
    def product_category(self, obj):
        return obj.product.category  # assuming category exists in DrugEntry
    product_category.short_description = 'Category'
    
    def product_price(self, obj):
        return obj.product.price  # assuming price exists in DrugEntry
    product_price.short_description = 'Price'
