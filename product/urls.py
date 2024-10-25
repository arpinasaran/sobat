from django.urls import path, include
from product.views import show_main, create_drug_entry
from product.views import show_xml, show_json, show_xml_by_id, show_json_by_id

app_name = 'product'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-drug-entry', create_drug_entry, name='create_drug_entry'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('xml/', show_json, name='show_xml'),
    path('json/', show_json, name='show_json'),
]