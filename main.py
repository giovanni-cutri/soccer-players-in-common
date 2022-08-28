import bs4
import requests
import lxml
import pickle

with open('resources/world_football_dict.pkl', 'rb') as f:
    world_football_dict = pickle.load(f)

print("Type the number of teams:")
number_of_teams = int(input())

teams = []

print("Type the names of the teams:")
for i in range(number_of_teams):
    teams.append(input())

team_players = []
players = []

for i in teams:
    link = world_football_dict[i]

    res = requests.get(link)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "lxml")
    players_elements = soup.select("a[href^='/player']")

    for j in players_elements:
        team_players.append(j.getText())
    players.append(team_players)
    team_players = []

for i in range(number_of_teams):
    players[i] = list(filter(None, players[i]))

print(sorted(list(set.intersection(*map(set, players)))))
