import requests
import json
import time
from Match import Match

api_key = ''
championsJSON = json.loads(requests.get('http://ddragon.leagueoflegends.com/cdn/8.24.1/data/en_US/champion.json').text)
champ_map = {}
games = {}


def request_summoner_data(region, summoner_name):
    URL = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + \
          summoner_name + "?api_key=" + api_key
    return requests.get(URL).json()


def account_id_from_summoner(summoner_json):
    return str(summoner_json['accountId'])


def id_from_summoner(summoner_json):
    return str(summoner_json['id'])


def request_league(region, id):
    URL = 'https://' + region + '.api.riotgames.com/lol/league/v4/leagues/' + id + "?api_key=" + api_key
    return requests.get(URL).json()


def request_match_list(region, id):
    URL = "https://" + region + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + id + "?api_key=" + api_key
    return requests.get(URL).json()


def request_match_info(region, match_id):
    match_id = str(match_id)
    URL = "https://" + region + ".api.riotgames.com/lol/match/v4/matches/" + match_id + "?api_key=" + api_key
    return requests.get(URL).json()


def request_recent_ranked_match_list(region, id):
    URL = "https://" + region + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + \
          id + "?queue=420&season=11&api_key=" + api_key
    return requests.get(URL).json()


def request_master_players(region):
    URL = "https://" + region + ".api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5" + \
          "?api_key=" + api_key
    masterJSON = requests.get(URL).json()

    masters = []
    for entry in masterJSON['entries']:
        masters.append(str(entry['summonerName']))

    return masters


def populate_champ_map():
    print('Generating Champion Map...')
    for majorkey, subdict in championsJSON.items():
        if majorkey == 'data':
            for subkey, value in subdict.items():
                champ_map[str(value['key'])] = value['id']
    print(champ_map)


def get_players_in_league(region, leagueId):
    players = []
    league = request_league(region, leagueId)
    for entry in league['entries']:
        print(entry['summonerName'])
        players.append(str(entry['summonerName']))
    return players


def create_match_obj_from_match(region, match, match_number):
    teams = []
    currTeam = []
    player_number = 0
    winner = None
    match_info_json = request_match_info(region, match['gameId'])
    # print(match_info_json)
    try:
        for participant in match_info_json['participants']:
            currChampId = participant['championId']
            currChamp = champ_map.get(str(currChampId))
            currTeam.append(str(currChamp))
            if player_number == 4 or player_number == 9:
                teams.append(currTeam)
                currTeam = []
                player_number = 0
                if winner is None:
                    winner = 0 if str(participant['stats']['win']) == 'True' else 1
            else:
                player_number += 1
    except KeyError:
        print(match_info_json)
    return Match(match_number, match['gameId'], teams, winner)


def save_matches_to_json(player_matches, filename):
    json_string = json.dumps([ob.__dict__ for ob in player_matches])
    with open(str(filename) + '.json', 'w') as outfile:
        outfile.write(json_string)


# NA1:
# 4ce7acd0-5974-11e8-819e-c81f66cf135e
# 99ea79e0-c689-11e8-b905-c81f66cf2333
# 92486ca0-fcf0-11e7-979b-c81f66dbb56c
# b66f6d70-1bb0-11e8-9727-c81f66cf135e

# d924ab30-33e0-11e8-80ab-c81f66cf135e
# 36689fd0-7442-11e8-b3c4-c81f66cf2333
# c9fdd1e0-fbfa-11e7-b4cc-c81f66cf2333
# 2bfd0760-faef-11e7-92d6-c81f66dbb56c

# feb6ad80-9948-11e8-8d1d-c81f66dbb56c

# EUW1:
# 102b5d00-fb8c-11e7-ba32-c81f66dacb22

# KR:
# 953b1df0-ccb0-11e8-b499-c81f66e3887d


def collect_match_data(region, league_id):
    players = get_players_in_league(region, league_id)
    league = request_league(region, league_id)
    player_matches = []
    iterations = 0
    for player in players:
        if iterations == 7:
            save_matches_to_json(player_matches, str(region + '_' + league['tier'] +
                                                     '_' + league_id + '_' + str(len(player_matches))))
            print('Sleeping...')
            time.sleep(121)
            iterations = 0
            print('Resuming...')
        summoner_data = request_summoner_data(region, player)
        summoner_id = account_id_from_summoner(summoner_data)
        match_list = request_recent_ranked_match_list(region, summoner_id)
        # match_list = request_match_list(region, summoner_id)
        try:
            for match in match_list['matches'][:10]:
                if str(match['queue']) == '420':
                    match_obj = create_match_obj_from_match(region, match, len(player_matches))
                    player_matches.append(match_obj)
                    time.sleep(0.05)
        except KeyError:
            print(match_list)
        time.sleep(1.1)
        iterations += 1
        json_string = json.dumps([ob.__dict__ for ob in player_matches])
        print(str(json_string))


def main():
    global api_key
    api_key = input("API Key: ")
    region = input("Region(na1, eun1, euw1, br1, tr1, oc1, ru, jp1, or kr: ")
    populate_champ_map()
    collect_match_data(region, '953b1df0-ccb0-11e8-b499-c81f66e3887d')
    # get_players_in_league('na1', '4ce7acd0-5974-11e8-819e-c81f66cf135e')
    # na_masters = request_master_players("na1")
    # print(request_summoner_data('na1', na_masters[0]))
    # masters_matches = []
    # iterations = 0
    # for player in na_masters:
    #     if iterations == 10:
    #         print('Sleeping...')
    #         time.sleep(121)
    #         iterations = 0
    #         print('Resuming...')
    #     summoner_data = request_summoner_data('na1', player)
    #     summoner_id = account_id_from_summoner(summoner_data)
    #     match_list = request_match_list('na1', summoner_id)
    #     try:
    #         for match in match_list['matches'][:10]:
    #             if str(match['queue']) == '420':
    #                 match_obj = create_match_obj_from_match('na1', match, len(masters_matches))
    #                 masters_matches.append(match_obj)
    #     except KeyError:
    #         print(match_list)
    #     time.sleep(1.25)
    #     iterations += 1
    #     json_string = json.dumps([ob.__dict__ for ob in masters_matches])
    #     print(str(json_string))
    # responseJSON = request_summoner_data(region, summoner_name)
    # print(responseJSON)
    # ID = str(responseJSON['accountId'])
    # matchListJSON = request_match_list(region, ID)
    # match_num = 0
    # for match in matchListJSON['matches']:
    #     if str(match['queue']) == '420' and str(match['gameId']) not in games:
    #         print(match)
    #         matchJSON = request_match_info(region, match['gameId'])
    #         # print(matchJSON)
    #         teams = []
    #         currTeam = []
    #         player_number = 0
    #         winner = None
    #         for participant in matchJSON['participants']:
    #             currChampId = participant['championId']
    #             currChamp = champ_map.get(str(currChampId))
    #             currTeam.append(str(currChamp))
    #             if player_number == 4 or player_number == 9:
    #                 teams.append(currTeam)
    #                 currTeam = []
    #                 player_number = 0
    #                 if winner is None:
    #                     winner = 0 if str(participant['stats']['win']) == 'True' else 1
    #             else:
    #                 player_number += 1
    #             # print(str(currChampId) + ", " + str(currChamp) + ", " + str(participant['stats']['win']))
    #         curr_match = Match(match_num, teams, winner)
    #         games[str(match['gameId'])] = curr_match
    #         #games.append(curr_match)
    #         match_num += 1
    #         print(curr_match.to_string())
    #         print('---------')


if __name__ == "__main__":
    main()
