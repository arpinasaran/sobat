from django.urls import path
from forum.views import show_forum

app_name = 'forum'

urlpatterns = [
    path('', show_forum, name='show_forum'),
]