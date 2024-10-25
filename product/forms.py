from django.forms import ModelForm
from product.models import DrugEntry

class DrugEntryForm(ModelForm):
    class Meta:
        model = DrugEntry
        fields = ["name", "desc", "category", "drug_type", "drug_form", "price", "availibility"]