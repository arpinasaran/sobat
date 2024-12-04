from django.urls import path
from .views import *

app_name = 'review'

urlpatterns = [
    path('', reviews, name='reviews'),
    path('<str:product_id>/', reviews, name='reviews'),
    path('<str:product_id>/create/', create_review, name='create_review'),
    path('<str:product_id>/<str:review_id>/edit/', edit_review, name='edit_review'),
    path('<str:product_id>/<str:review_id>/delete/', delete_review, name='delete_review'),
    path('<str:product_id>/json/', reviews_json, name='reviews_json'),
]