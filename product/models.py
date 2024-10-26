from django.db import models
import uuid

class DrugEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    name = models.CharField(max_length=63)
    desc = models.TextField()
    category = models.CharField(max_length=63)
    drug_type = models.CharField(max_length=31)
    drug_form = models.CharField(max_length=31)
    price = models.IntegerField()
    availibility = models.BooleanField(default=True)
    # shop = models.ForeignKey('shop.ShopEntry', on_delete=models.RESTRICT, related_name='shop')
    image = models.ImageField(upload_to='')

    def __str__(self):
        return self.name
