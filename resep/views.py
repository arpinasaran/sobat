from django.shortcuts import render
from resep.models import Resep

def show_resep(request):
    resep = Resep.objects.all();

    context = {
        'resep': resep
    }

    return render(request, "resep.html", context)