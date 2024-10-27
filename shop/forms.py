# forms.py
from django import forms
from .models import ShopProfile, ShopProduct
from product.models import DrugEntry

class ShopProfileForm(forms.ModelForm):
    class Meta:
        model = ShopProfile
        fields = ['name', 'profile_image', 'address', 'opening_time', 'closing_time']
        widgets = {
            'opening_time': forms.TimeInput(attrs={'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class ManageProductForm(forms.Form):
    selected_products = forms.ModelMultipleChoiceField(
        queryset=DrugEntry.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        shop = kwargs.pop('shop', None)
        super(ManageProductForm, self).__init__(*args, **kwargs)
        if shop:
            initial_products = DrugEntry.objects.filter(shop_products__shop=shop)
            self.fields['selected_products'].initial = initial_products