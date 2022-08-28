import requests
import bs4
import lxml

leagues = ["https://www.worldfootball.net/alltime_table/eng-premier-league/",
           "https://www.worldfootball.net/alltime_table/bundesliga/",
           "https://www.worldfootball.net/alltime_table/esp-primera-division/",
           "https://www.worldfootball.net/alltime_table/ita-serie-a/",
           "https://www.worldfootball.net/alltime_table/fra-ligue-1/",
           "https://www.worldfootball.net/alltime_table/tur-sueperlig/",
           "https://www.worldfootball.net/alltime_table/ned-eredivisie/",
           "https://www.worldfootball.net/alltime_table/sco-premiership/",
           "https://www.worldfootball.net/alltime_table/aut-bundesliga/"]

teams_names_raw = []
teams_links_raw = []

worldfootball_dict = {

}

for i in leagues:
    res = requests.get(i)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "lxml")
    teams_elements = soup.select("td a[href^='/teams/']")
    for j in teams_elements:
        teams_names_raw.append(j.getText())
        teams_links_raw.append("https://www.worldfootball.net" + j.attrs["href"])

teams_names = list(filter(None, teams_names_raw))
teams_links = list(dict.fromkeys(teams_links_raw))

worldfootball_dict = dict(zip(teams_names, teams_links))

print(worldfootball_dict)