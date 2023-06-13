from django.shortcuts import render
from .models import Team

# Create your views here.

def index(request):
    return render(request, "soccer_players/index.html", {
        "teams": Team.objects.all()
    })