from django.shortcuts import render
from .models import Team

import requests
import bs4

# Create your views here.

def index(request):
    return render(request, "soccer_players/index.html", {
        "number": range(2),
        "teams": Team.objects.all().order_by("name")
    })

def number(request, num):
    return render(request, "soccer_players/teams.html", {
        "number": num,
        "teams": Team.objects.all().order_by("name")
    })

def players(request):
    if request.method == "POST":
        teams = []
        for team in request.POST:
            teams.append(request.POST[team])
        teams = teams[1:] # remove CRSF token
        team_players = []
        players = []

        for i in teams:
            res = requests.get(i)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text, "lxml")
            players_elements = soup.select("a[href^='/player']")

            for j in players_elements:
                team_players.append("https://www.worldfootball.net" + j.attrs["href"])
            players.append(team_players)
            team_players = []

        for i in range(len(teams)):
            players[i] = list(filter(None, players[i]))

        unsorted_players_in_common = list(set.intersection(*map(set, players)))

        players_in_common = sorted(unsorted_players_in_common)
 
        players = []
        for player in players_in_common:
            res = requests.get(player)
            soup = bs4.BeautifulSoup(res.text)
            element = soup.select("div[itemtype='http://schema.org/Person']")[0]
            players.append(str(element))

        return render(request, "soccer_players/players.html", {
            "players": players
        })