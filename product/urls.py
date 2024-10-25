from django.urls import path, include
from product.views import show_main, create_drug, edit_drug, delete_drug, show_drug
from product.views import show_xml, show_json, show_xml_by_id, show_json_by_id
from product.views import create_drug_ajax, edit_drug_ajax

app_name = 'product'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-drug/', create_drug, name='create_drug'),
    path('create-drug-ajax/', create_drug_ajax, name='create_drug_ajax'),
    path('edit-drug-ajax/<str:id>/', edit_drug_ajax, name='edit_drug_ajax'),
    path('edit-drug/<str:id>/', edit_drug, name='edit_drug'),
    path('delete-drug/<str:id>/', delete_drug, name='delete_drug'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('xml/', show_json, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('view-drug/<str:id>/', show_drug, name='show_drug'),
]