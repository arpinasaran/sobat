from django.forms import ModelForm
from forum.models import Pertanyaan, Jawaban

class PertanyaanForm(ModelForm):
    class Meta:
        model = Pertanyaan
        fields = ["mood", "feelings", "mood_intensity"]

class JawabanForm(ModelForm):
    class Meta:
        model = Jawaban
        fields = ["mood", "feelings", "mood_intensity"]