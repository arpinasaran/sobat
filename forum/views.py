from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from forum.models import Question, Answer
from django.core import serializers
from forum.forms import QuestionForm, AnswerForm
from product.models import DrugEntry
import json

@login_required(login_url='/login')
def show_forum(request):
    user = request.user
    context = {
        'user': user,
        'user_pk': user.pk,
    }
    return render(request, "forum.html", context)

@login_required(login_url='/login')
def add_question(request):
    user = request.user

    context = {
        'user': user,
        'user_pk': user.pk,
    }
    return render(request, "add_question.html", context)

@login_required(login_url='/login')
def show_answers(request, id):
    user = request.user
    question = get_object_or_404(Question, pk=id)

    context = {
        'user': user,
        'user_pk': user.pk,
        'question_pk': question.pk,
    }
    return render(request, "answers.html", context)

@csrf_exempt
@login_required(login_url='/login')
def add_question_ajax(request, id):
    form = QuestionForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        chosen_product = None
        if id and id != "null":
            chosen_product = DrugEntry.objects.get(pk=id)
        new_question = form.save(commit=False)
        new_question.drug_asked = chosen_product
        new_question.user = request.user

        new_question.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
def add_question_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        new_question = Question.objects.create(
            user=request.user,
            drug_asked=None,
            question_title="ambas",
            question="onyong",
        )

        new_question.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
@login_required(login_url='/login')
def answer_question(request, questionId, productId):
    form = AnswerForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        chosen_product = None
        if productId and productId != "null":
            chosen_product = DrugEntry.objects.get(pk=productId)
        new_answer = form.save(commit=False)
        question = Question.objects.get(pk=questionId)
        new_answer.question = question
        new_answer.drug_ans = chosen_product
        new_answer.user = request.user

        new_answer.save()

        question.num_answer += 1  # Increment answer count
        question.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
@login_required(login_url='/login')
def like_question(request, id):
    if request.method == 'POST':
        question = Question.objects.get(pk=id)
        user = request.user
        
        if user in question.likes.all():
            question.likes.remove(user)
            is_liked = False
        else:
            question.likes.add(user)
            is_liked = True
            
        return JsonResponse({
            'status': 'success',
            'like_count': question.likes.count(),
            'is_liked': is_liked
        })

@csrf_exempt
@login_required(login_url='/login')
def delete_question(request, id):
    if request.method == 'DELETE':
        question = Question.objects.get(pk=id)
        question.delete()
        return HttpResponse(b"DELETED", status=200)
    
    return HttpResponseNotFound()

@csrf_exempt
@login_required(login_url='/login')
def like_answer(request, id):
    if request.method == 'POST':
        answer = Answer.objects.get(pk=id)
        user = request.user
        
        if user in answer.likes.all():
            answer.likes.remove(user)
            is_liked = False
        else:
            answer.likes.add(user)
            is_liked = True
            
        return JsonResponse({
            'status': 'success',
            'like_count': answer.likes.count(),
            'is_liked': is_liked
        })

@csrf_exempt
@login_required(login_url='/login')
def delete_answer(request, id):
    if request.method == 'DELETE':
        answer = Answer.objects.get(pk=id)
        question = answer.question
        question.num_answer -= 1  # Decrement answer count
        question.save()
        answer.delete()
        return HttpResponse(b"DELETED", status=200)
    
    return HttpResponseNotFound()

def show_json_question(request):
    questions = Question.objects.select_related('user').all()  # Use select_related for optimization
    data = []

    for question in questions:
        question_data = {
            "pk": str(question.id),
            "fields": {
                "user": question.user.id,  # Include user ID
                "username": question.user.username,  # Include username
                "role": question.user.role,
                "drug_asked": str(question.drug_asked.id) if question.drug_asked else "",
                "question_title": question.question_title,
                "question": question.question,
                "likes": list(question.likes.values_list('id', flat=True)),
                "num_likes": question.likes.count(),
                "num_answer": question.num_answer,
            }
        }
        data.append(question_data)

    return JsonResponse(data, safe=False)  # Using JsonResponse to return the custom data

def show_json_answer(request, id):
    answers = Answer.objects.filter(question=id)  # Use select_related for optimization
    data = []

    for answer in answers:
        answer_data = {
            "pk": str(answer.id),
            "fields": {
                "user": request.user.id,  # Include user ID
                "username": answer.user.username,  # Include username
                "role": answer.user.role,
                "drug_ans": str(answer.drug_ans.id) if answer.drug_ans else None,
                "question": answer.question.pk,
                "answer": answer.answer,
                "likes": list(answer.likes.values_list('id', flat=True)),
                "num_likes": answer.likes.count()
            }
        }
        data.append(answer_data)

    return JsonResponse(data, safe=False)  # Using JsonResponse to return the custom data

def show_json_question_by_id(request, id):
    questions = Question.objects.filter(pk=id)
    data = []
    for question in questions:
        question_data = {
            "pk": str(question.id),
            "fields": {
                "user": question.user.id,  # Include user ID
                "username": question.user.username,  # Include username
                "role": question.user.role,
                "drug_asked": str(question.drug_asked.id) if question.drug_asked else None,
                "question_title": question.question_title,
                "question": question.question,
                "likes": list(question.likes.values_list('id', flat=True)),
                "num_likes": question.likes.count(),
                "num_answer": question.num_answer,
            }
        }
        data.append(question_data)

    return JsonResponse(data, safe=False)

