import argparse
import bs4
import requests
import pickle


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--country", help="the country of the players")
    parser.add_argument("-p", "--position", help="the position of the players")
    args = parser.parse_args()
    return args


def import_dictionary():
    with open('resources/world_football_dict.pkl', 'rb') as f:
        world_football_dict = pickle.load(f)
        return world_football_dict


def get_number_of_teams():
    number_of_teams = int(input("Type the number of teams: "))
    return number_of_teams


def get_teams(number_of_teams):
    teams = []
    print("\nType the names of the teams:")
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
            name = j.getText()
            info = j.find_all_next("td")
            country = info[1].getText()
            position = info[2].getText()
            player = {
                "name": name,
                "country": country,
                "position": position
            }
            team_players.append(player)         # get players of a single team
        players.append(team_players)            # append players of the team to the collective list of players
        team_players = []                       # empty list of the players of the single team

    for i in range(number_of_teams):
        players[i] = list(filter(None, players[i]))     # remove empty values

    return players


def get_players_in_common(players):
    unsorted_players_in_common =  players[0]
    for counter, _ in enumerate(players):
        try:
            unsorted_players_in_common = [player for player in unsorted_players_in_common if player in players[counter + 1]]
        except IndexError:
            break

    players_in_common = sorted(unsorted_players_in_common, key = lambda x: x["name"])

    return players_in_common


def filter_country(players, country):
    for player in players.copy():
        if player["country"].lower() != country.lower():
            players.remove(player)
    return players


def filter_position(players, position):
    for player in players.copy():
        if player["position"].lower() != position.lower():
            players.remove(player)
    return players


def print_players(players):
    if not players:
        print("\nNo players found.")
    else:
        print("\nPlayers in common between the teams:\n")
        for player in players:
            print('{:40s} {:30s}  {:20s}'.format(player["name"], player["country"], player["position"]))
        


def main():
    args = parse_arguments()
    world_football_dict = import_dictionary()
    number_of_teams = get_number_of_teams()
    teams = get_teams(number_of_teams)
    players = get_players(teams, world_football_dict, number_of_teams)
    players_in_common = get_players_in_common(players)
    if args.country:
        country = args.country
        players_in_common = filter_country(players_in_common, country)
    if args.position:
        position = args.position
        players_in_common = filter_position(players_in_common, position)
    print_players(players_in_common)


if __name__ == "__main__":
    main()
