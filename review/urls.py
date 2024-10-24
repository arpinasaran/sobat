from django.urls import path
from .views import *

app_name = 'review'

urlpatterns = [
    path('', reviews, name='reviews'),
    path('<uuid:product_id>/', reviews, name='reviews'),
    path('<uuid:product_id>/json/', reviews_json, name='reviews_json'),
    path('<uuid:product_id>/create/', create_review, name='create_review'),
    path('<uuid:product_id>/create_ajax/', create_review_ajax, name='create_review_ajax'),
    path('<uuid:review_id>/edit/', edit_review, name='edit_review'),
]