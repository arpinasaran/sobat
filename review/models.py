from django.db import models
from authentication.models import User
from product.models import DrugEntry as Produk
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Produk, on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} Review: {self.rating} Star(s) - {self.reviewer.username}"
