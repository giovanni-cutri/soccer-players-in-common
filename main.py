import bs4
import requests
import lxml

players = []

res = requests.get("https://www.worldfootball.net/teams/ac-milan/10/")
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "lxml")

player_elements = soup.select("a[href^='/player']")

for i in player_elements:
    players.append(i.getText())

print(players)