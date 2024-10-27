from django.urls import path
from forum.views import *

app_name = 'forum'

urlpatterns = [
    path('', show_forum, name='show_forum'),
    path('add_question/', add_question, name='add_question'),
    path('add_question_ajax/<str:id>/', add_question_ajax, name='add_question_ajax'),
    path('like_question/<str:id>/', like_question, name='like_question'),
    path('like_answer/<str:id>/', like_answer, name='like_answer'),
    path('delete_question/<str:id>/', delete_question, name='delete_question'),
    path('delete_answer/<str:id>/', delete_answer, name='delete_answer'),
    path('answer_question/<str:questionId>/<str:productId>/', answer_question, name='answer_question'),
    path('show_answers/<str:id>/', show_answers, name='show_answers'),
    path('xml/', show_xml, name='show_xml'),
    path('show_json_answer/<str:id>/', show_json_answer, name='show_json_answer'),
    path('json/', show_json_question, name='show_json_question'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_question_by_id, name='show_json_question_by_id'),
]