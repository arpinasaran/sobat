from django.db import models
from authentication.models import User
from product.models import DrugEntry as Produk
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

class Resep(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Produk, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)])

    def __str__(self):
        return f"{self.product.name} - {self.amount}"
