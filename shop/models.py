# shop/models.py
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.owner.username}"

class ShopProduct(DrugEntry):
    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = 'shop_shopproduct'

    def __str__(self):
        return f"{self.name} - {self.shop.name}"