from django.urls import path
from .views import *

urlpatterns = [
    path('product/<uuid:product_id>/reviews/', reviews, name='reviews'),
    path('product/<uuid:product_id>/reviews/create/', create_review, name='create_review'),
]