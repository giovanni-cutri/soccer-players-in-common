import requests
import bs4
import lxml
import pickle

site_domain = "https://www.worldfootball.net"

all_leagues_page = "https://www.worldfootball.net/continents/uefa/"
# despite referring only to UEFA, actually contains links for competitions all over the world

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

teams_names_raw = []
teams_links_raw = []

world_football_dict = {

}

for i in all_time_league_tables:
    print("Currently at " + i)
    res = requests.get(i)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "lxml")
    teams_elements = soup.select("td a[href^='/teams/']")
    for j in teams_elements:
        if j.getText() not in teams_names_raw:
            teams_names_raw.append(j.getText())
            teams_links_raw.append("https://www.worldfootball.net" + j.attrs["href"])

teams_names = list(filter(None, teams_names_raw))
teams_links = list(dict.fromkeys(teams_links_raw))

teams_players = []

for i in teams_links:
    teams_players.append(i + "10/")

world_football_dict = dict(zip(teams_names, teams_players))

with open('world_football_dict.pkl', 'wb') as f:
    pickle.dump(world_football_dict, f)
