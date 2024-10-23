from django.shortcuts import render

# Create your views here.
def show_forum(request):
    context = {
        'npm' : '2306123456',
        'name': 'Pak Bepe',
        'class': 'PBP E'
    }

    return render(request, "forum.html", context)