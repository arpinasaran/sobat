from django.db import models
from authentication.models import User
from product.models import DrugEntry
import uuid

class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drug_asked = models.ForeignKey(DrugEntry, on_delete=models.CASCADE, null=True)
    question_title = models.CharField(max_length=255)
    question = models.TextField()
    likes = models.ManyToManyField(User, related_name='question_like')
    num_answer = models.IntegerField(default=0)

class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers_question', on_delete=models.CASCADE)
    answer = models.TextField()
    drug_ans = models.ForeignKey(DrugEntry, on_delete=models.CASCADE, null=True)
    likes = models.ManyToManyField(User, related_name='answer_like')
