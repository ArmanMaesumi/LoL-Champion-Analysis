class Match:

    def __init__(self, match_num, match_id, teams, winner):
        self.match_num = match_num
        self.match_id = match_id
        self.teams = teams
        self.winner = winner

    def __repr__(self):
        return str(self.match_num) + ": " + str(self.teams) + ": Winner=" + str(self.winner)

    def contains_champ(self, tgt):
        return any(tgt in sublist for sublist in self.teams)

    def contains_champs(self, champs):
        for champ in champs:
            if not self.contains_champ(champ):
                return False
        return True

    def contains_composition(self, champs):
        if len(champs) == 1:
            return self.contains_champs(champs[0])

        if all(champ in self.teams[0] for champ in champs[0]) \
                and all(champ in self.teams[1] for champ in champs[1]):
            return True
        elif all(champ in self.teams[1] for champ in champs[0]) \
                and all(champ in self.teams[0] for champ in champs[1]):
            return True
        else:
            return False

    def champ_won(self, tgt):
        if self.winner == str(0):
            return tgt in self.teams[0]
        else:
            return tgt in self.teams[1]
