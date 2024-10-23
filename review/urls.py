from django.urls import path
from .views import reviews, create_review

app_name = 'review'

urlpatterns = [
    path('display-reviews/', reviews, name='reviews'),
    path('<uuid:product_id>/display-reviews/', reviews, name='reviews'),
    path('<uuid:product_id>/display-reviews/create/', create_review, name='create_review'),
]