from django.forms import ModelForm
from forum.models import Question, Answer

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ["question_title", "question"]

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ["answer"]