from django.forms import ModelForm
from django import forms
from .models import Review
from django.utils.html import strip_tags

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'w-full p-2 border border-black rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Enter your rating',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-black rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Enter your review',
            }),
        }

    def clean_comment(self):
        return strip_tags(self.cleaned_data["comment"])