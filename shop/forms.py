# shop/forms.py
from django import forms
from product.forms import DrugEntryForm
from .models import ShopProfile, ShopProduct

class ShopProfileForm(forms.ModelForm):
    class Meta:
        model = ShopProfile
        fields = ['name', 'profile_image', 'address', 'opening_time', 'closing_time']
        widgets = {
            'opening_time': forms.TimeInput(attrs={'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class ShopProductForm(DrugEntryForm):
    class Meta(DrugEntryForm.Meta):
        model = ShopProduct
        fields = DrugEntryForm.Meta.fields + ['image']  # Menambahkan field tambahan yang ada di shop