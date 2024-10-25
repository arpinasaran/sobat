from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from forum.models import Question
from django.core import serializers
from forum.forms import QuestionForm, AnswerForm

@login_required(login_url='/login')
def show_forum(request):
    return render(request, "forum.html")

def add_question(request):
    form = QuestionForm(request.POST or None)
    
    if form.is_valid() and request.method == "POST":
        mood_entry = form.save(commit=False)
        mood_entry.user = request.user
        mood_entry.save()
        return redirect('forum:show_forum')

    context = {'form': form}
    return render(request, "add_question.html", context)

@csrf_exempt
@require_POST
def add_question_ajax(request):
    user = request.user
    drug_asked = request.POST.get("drug_asked")
    question_title = request.POST.get("question_title")
    question = request.POST.get("question")

    new_question = Question(
        user=user, drug_asked=drug_asked,
        question_title=question_title, question=question,
        likes=0,answered=False
    )
    new_question.save()

    return HttpResponse(b"CREATED", status=201)

def show_xml(request):
    data = Question.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Question.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Question.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Question.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
