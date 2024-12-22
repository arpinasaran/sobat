from django.urls import path, include
from resep.views import show_resep, update_amount, add_to_resep, clear_recipes, show_json, show_json_by_id

app_name = 'resep'

urlpatterns = [
    path('', show_resep, name='show_resep'),
    path('update/', update_amount, name='update_amount'),
    path('add/<uuid:product_id>/', add_to_resep, name='add_to_resep'),
    path('clear/', clear_recipes, name='clear_recipes'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('json/', show_json, name='show_json'),
]