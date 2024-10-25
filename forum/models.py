from django.db import models
from authentication.models import User
from product.models import DrugEntry
import uuid

class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drug_asked = models.ForeignKey(DrugEntry, on_delete=models.CASCADE)
    question_title = models.CharField(max_length=100)
    question = models.TextField()
    likes = models.ManyToManyField(User, related_name='question_like')

class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    answer = models.TextField()
    drug_ans = models.ForeignKey(DrugEntry, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='answer_like')
