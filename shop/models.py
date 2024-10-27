from django.db import models
from django.conf import settings
from product.models import DrugEntry
import uuid

class ShopProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shops')
    name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='shop_profiles/', null=True, blank=True)
    address = models.TextField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    products = models.ManyToManyField(DrugEntry, through='ShopProduct')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.owner.username}"

class ShopProduct(models.Model):
    # Menggunakan AutoField sebagai primary key default
    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE, related_name='shop_products')
    product = models.ForeignKey(DrugEntry, on_delete=models.CASCADE, related_name='shop_products')
    stock = models.PositiveIntegerField(default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['shop', 'product']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} at {self.shop.name}"