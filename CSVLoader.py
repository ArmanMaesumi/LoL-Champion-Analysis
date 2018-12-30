import pandas
import os
from Match import Match

col_names = ['match_num', 'teams', 'match_id', 'winner']
match_map = {}


def get_match_map_from_csv():
    data = pandas.read_csv('na_data2.csv', names=col_names)
    ids = data['match_id'].values
    print(str(len(ids)) + " total matches.")
    id_set = set(ids)
    print(str(len(id_set)) + " unique matches.")
    for index, row in data.iterrows():
        curr_id = row['match_id']
        curr_team = row['teams'].split(',')
        teams = [curr_team[0:5], curr_team[5:10]]
        if curr_id not in match_map:
            match_map[curr_id] = Match(row['match_num'], row['match_id'], teams, row['winner'])
    return match_map


def multiple_csv_to_match_map(file_names):
    for file in file_names:
        data = pandas.read_csv(str(file), names=col_names)
        ids = data['match_id'].values
        print(str(len(ids)) + " total matches.")
        id_set = set(ids)
        print(str(len(id_set)) + " unique matches.")
        for index, row in data.iterrows():
            curr_id = row['match_id']
            curr_team = row['teams'].split(',')
            teams = [curr_team[0:5], curr_team[5:10]]
            if curr_id not in match_map:
                match_map[curr_id] = Match(row['match_num'], row['match_id'], teams, row['winner'])
    return match_map


def load_cvs_in_dir(dir):
    files = os.listdir(dir)
    for i in range(len(files)):
        files[i] = dir + files[i]
    print(files)
    return multiple_csv_to_match_map(files)
