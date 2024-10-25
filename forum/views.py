from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from forum.models import Question, Answer
from django.core import serializers
from forum.forms import QuestionForm, AnswerForm
from product.models import DrugEntry

@login_required(login_url='/login')
def show_forum(request):
    return render(request, "forum.html")

@login_required(login_url='/login')
def add_question(request):
    form = QuestionForm(request.POST or None)
    
    if form.is_valid() and request.method == "POST":
        new_question = form.save(commit=False)
        new_question.user = request.user
        new_question.save()
        return redirect('forum:show_forum')

    context = {'form': form}
    return render(request, "add_question.html", context)

@csrf_exempt
def add_question_ajax(request, id):
    form = QuestionForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        chosen_product = DrugEntry.objects.get(pk=id)
        new_question = form.save(commit=False)
        new_question.drug_asked = chosen_product
        new_question.user = request.user
        
        new_question.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()
    # user = request.user
    # drug_asked = request.POST.get("drug_asked")
    # question_title = request.POST.get("question_title")
    # question = request.POST.get("question")

    # new_question = Question(
    #     user=user, drug_asked=drug_asked,
    #     question_title=question_title, question=question,
    #     likes=0,answered=False
    # )
    # new_question.save()

    # return HttpResponse(b"CREATED", status=201)

@login_required(login_url='/login')
def like_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    # Toggle like
    if request.user in question.likes.all():
        question.likes.remove(request.user)
        liked = False
    else:
        question.likes.add(request.user)
        liked = True

    return JsonResponse({"liked": liked, "likes_count": question.likes.count()})

@login_required(login_url='/login')
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)

    # Toggle like
    if request.user in answer.likes.all():
        answer.likes.remove(request.user)
        liked = False
    else:
        answer.likes.add(request.user)
        liked = True

    return JsonResponse({"liked": liked, "likes_count": answer.likes.count()})


def show_xml(request):
    data = Question.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_question(request):
    data = Question.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Question.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Question.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
