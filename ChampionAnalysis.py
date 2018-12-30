import CSVLoader
import json
import requests
import operator
import itertools

match_map = {}
champ_map = {}


def populate_champ_map():
    championsJSON = json.loads(
        requests.get('http://ddragon.leagueoflegends.com/cdn/8.24.1/data/en_US/champion.json').text)
    print('Generating Champion Map...')
    for majorkey, subdict in championsJSON.items():
        if majorkey == 'data':
            for subkey, value in subdict.items():
                champ_map[str(value['key'])] = value['id']


def load_csv():
    global match_map
    # match_map = CSVLoader.multiple_csv_to_match_map(['na_data2.csv', 'na_diamond.csv'])
    match_map = CSVLoader.load_cvs_in_dir('data/')


def champ_win_rate_versus(champ, other_champ):
    win = 0
    lost = 0
    for key, value in match_map.items():
        if value.contains_composition([[champ], [other_champ]]):
            if value.champ_won(champ):
                win += 1
            else:
                lost += 1
    print(champ + "(" + str(win) + ") vs. " + other_champ + "(" + str(lost) + "): " + str(
        (win / (win + lost)) * 100) + "%")


def champ_win_rate_in_comp(champ, composition):
    win = 0
    lost = 0
    for key, value in match_map.items():
        if value.contains_composition(composition):
            # print(value)
            if value.champ_won(champ):
                win += 1
            else:
                lost += 1
    # if (win + lost) == 0:
    #     return 0
    # win_rate = (win / (win + lost)) * 100
    # print(champ + " in " + str(composition) + "(" + str(win) + "/" + str(lost+win) + "): " + str(win_rate) + "%")
    return [win, lost, win + lost]


def analyze(on_blue_team, composition):
    champ_scores = {}
    champ_team_assignment = {}
    champ_list = []
    blue_team = composition[0]
    red_team = composition[1]
    for champ in blue_team:
        champ_team_assignment[champ] = 'B'
        champ_list.append(champ)
    for champ in red_team:
        champ_team_assignment[champ] = 'R'
        champ_list.append(champ)

    for champion_id in champ_map:
        curr_champion = champ_map.get(champion_id)
        if curr_champion in champ_list:
            continue

        curr_champ_score = champ_scores.get(curr_champion)
        if curr_champ_score is None:
            curr_champ_score = 0
            champ_scores[curr_champion] = 0

        for i in range(len(champ_list) + 1):
            if i > 0:
                combinations = list(itertools.combinations(champ_list, i))
                for element in combinations:
                    combination = list(element)
                    new_comp = [[], []]

                    if on_blue_team:
                        new_comp[0].append(curr_champion)
                    else:
                        new_comp[1].append(curr_champion)

                    for champ in combination:
                        team = 0 if champ in blue_team else 1
                        if team == 0:
                            new_comp[0].append(champ)
                        else:
                            new_comp[1].append(champ)
                    win_rate = champ_win_rate_in_comp(curr_champion, new_comp)
                    curr_champ_score += (win_rate[0] - win_rate[1]) * win_rate[2]

        champ_scores[curr_champion] = curr_champ_score

    print(champ_scores)
    sorted_map = sorted(champ_scores.items(), key=operator.itemgetter(1))
    print(sorted_map)
    # for champion_id in champ_map:
    #     champion = champ_map.get(champion_id)
    #     new_comp = copy.deepcopy(composition)
    #     if on_blue_team:
    #         new_comp[0].append(champion)
    #     else:
    #         new_comp[1].append(champion)
    #     win_rate = champ_win_rate_in_comp(champion, new_comp)
    #     champ_win_rates[champion] = win_rate
    # sorted_map = sorted(champ_win_rates.items(), key=operator.itemgetter(1))
    # print(sorted_map)


if __name__ == '__main__':
    load_csv()
    populate_champ_map()
    print('Sample size: ' + str(len(match_map)))

    # Display [win, lost, total] record for Lucian against Thresh and Ahri:
    print(champ_win_rate_in_comp('Lucian', [['Lucian'], ['Thresh', 'Ahri']]))

    # Display [win, lost, total] record for Jax with Lucian on the same team:
    print(champ_win_rate_in_comp('Jax', [['Jax', 'Lucian'], []]))

    # Find best champions for blue side in composition:
    analyze(True, [['Lucian', 'Graves'], ['Irelia']])
