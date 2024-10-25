from django.db import models
from authentication.models import User
import uuid
from product.models import DrugEntry



class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(DrugEntry, on_delete=models.CASCADE)
    # date_added = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

# Create your models here.
