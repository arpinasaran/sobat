from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/login')
def show_main(request):

    context = {
        'name': request.user.username,
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "main.html", context)