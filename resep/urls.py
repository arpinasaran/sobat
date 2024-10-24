from django.urls import path, include
from resep.views import show_resep

app_name = 'resep'

urlpatterns = [
    path('', show_resep, name='show_resep'),
]