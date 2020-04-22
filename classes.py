class team:
    def __init__(self, name):
        self.name = name
        self.possession = 0
        self.onTarget = 0
        self.offTarget = 0
        self.goalsFor = 0
        self.goalsAgainst = 0
        self.goalD = 0 
        self.fifaRank = 0
        self.euroRank = 0
        self.networkRank = 0
        self.group = ''
        self.matchesPlayed = 0
        self.rating = 0
        self.form = []
        self.teamID = 0

class match:
    def __init__(self, group, teamOne, teamTwo, winner, matchID):
        self.teamOne = teamOne
        self.teamTwo = teamTwo
        self.winner = winner
        self.group = group
        self.matchID = matchID


    


