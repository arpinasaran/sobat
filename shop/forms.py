from django import forms
from .models import ShopProfile, Product

class ShopProfileForm(forms.ModelForm):
    class Meta:
        model = ShopProfile
        fields = ['name', 'profile_image', 'address', 'opening_time', 'closing_time']
        widgets = {
            'opening_time': forms.TimeInput(attrs={'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'drug_type', 'medium', 'price', 
                 'description', 'dosage', 'is_available', 'image']