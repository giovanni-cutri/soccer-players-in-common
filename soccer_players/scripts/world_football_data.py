import requests
import bs4
import json
from itertools import islice

site_domain = "https://www.worldfootball.net"

all_leagues_page = "https://www.worldfootball.net/continents/uefa/"

res = requests.get(all_leagues_page)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "lxml")

leagues_tag_objects = soup.select("a[href^='/competition']")

leagues = []

for i in leagues_tag_objects:
    partial_link = i.attrs["href"]
    leagues.append(site_domain + partial_link)

leagues = list(dict.fromkeys(leagues))
all_time_league_tables = []

for i in leagues:

    print("Currently at " + i)

    try:
        res = requests.get(i)
        res.raise_for_status()
    except requests.exceptions.HTTPError:
        print("HTTP Error 500: Internal Server Error")
        continue
    soup = bs4.BeautifulSoup(res.text, "lxml")

    all_time_league_tables_tag_objects = soup.select("a[href^='/alltime_table']")
    if all_time_league_tables_tag_objects:
        partial_link = all_time_league_tables_tag_objects[0].attrs["href"]
        all_time_league_tables.append(site_domain + partial_link)

all_time_league_tables = list(dict.fromkeys(all_time_league_tables))

world_football_data = []

links = []
pk = 1

for i in all_time_league_tables:
    print("Currently at " + i)
    res = requests.get(i)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "lxml")
    teams_elements = soup.select("td a[href^='/teams/'] img")
    for j in teams_elements:
        team_name = j.attrs["alt"]
        team_image = j.attrs["src"]
        team_link = "https://www.worldfootball.net/teams/" + j.attrs["alt"].lower().replace(" ", "-") + "/"
        if team_link not in links:
            links.append(team_link)
            temp_dict = {
                "model": "soccer_players.team",
                "pk": pk,
                "fields": {
                    "name": team_name,
                    "image": team_image,
                    "link": team_link
                }
            }
            world_football_data.append(temp_dict)
            pk = pk + 1

with open('../fixtures/world_football_data.json', 'w') as f:
    json.dump(world_football_data, f)