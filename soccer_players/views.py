from django.shortcuts import render
teams = ["Bayern", "Barcellona"]
# Create your views here.

def index(request):
    return render(request, "soccer_players/index.html", {
        "teams": teams
    })