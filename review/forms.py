from django.forms import ModelForm
from .models import Review
from django.utils.html import strip_tags

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

    def clean_comment(self):
        return strip_tags(self.cleaned_data["comment"])