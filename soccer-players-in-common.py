import bs4
import requests
import pickle


def import_dictionary():
    with open('resources/world_football_dict.pkl', 'rb') as f:
        world_football_dict = pickle.load(f)
        return world_football_dict


def get_number_of_teams():
    print("Type the number of teams:")
    number_of_teams = int(input())
    return number_of_teams


def get_teams(number_of_teams):
    teams = []
    print("Type the names of the teams:")
    for i in range(number_of_teams):
        teams.append(input())
    return teams


def get_players(teams, world_football_dict, number_of_teams):
    team_players = []   # players of each single team
    players = []        # players of all the teams combined

    for i in teams:
        link = world_football_dict[i]

        res = requests.get(link)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "lxml")
        players_elements = soup.select("a[href^='/player']")

        for j in players_elements:
            team_players.append(j.getText())    # get players of a single team
        players.append(team_players)            # append players of the team to the collective list of players
        team_players = []                       # empty list of the players of the single team

    for i in range(number_of_teams):
        players[i] = list(filter(None, players[i]))     # remove empty values

    return players


def get_players_in_common(players):
    unsorted_players_in_common = list(set.intersection(*map(set, players)))
    players_in_common = sorted(unsorted_players_in_common)
    return players_in_common


def print_players_in_common(players_in_common):
    print(players_in_common)


def main():
    world_football_dict = import_dictionary()
    number_of_teams = get_number_of_teams()
    teams = get_teams(number_of_teams)
    players = get_players(teams, world_football_dict, number_of_teams)
    players_in_common = get_players_in_common(players)
    print_players_in_common(players_in_common)


main()
