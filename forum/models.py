from django.db import models
from authentication.models import User
from product.models import DrugEntry
# from toko.models import Toko
# from resep.models import Resep
import uuid

# Create your models here.
class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drug_asked = models.ForeignKey(DrugEntry, on_delete=models.CASCADE)
    # toko_tanya = models.ForeignKey(Toko, on_delete=models.CASCADE)
    # resep_tanya = models.ForeignKey(Resep, on_delete=models.CASCADE)
    question_title = models.CharField(max_length=100)
    question = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    answered = models.BooleanField(default=False)

class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    drug_ans = models.ForeignKey(DrugEntry, on_delete=models.CASCADE)
    # toko_jawab = models.ForeignKey(Toko, on_delete=models.CASCADE)
    # resep_jawab = models.ForeignKey(Resep, on_delete=models.CASCADE)