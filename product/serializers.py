from rest_framework import serializers
from .models import DrugEntry

class DrugEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugEntry
        fields = ['id', 'name', 'desc', 'category', 'drug_type', 'drug_form', 'price', 'image']
