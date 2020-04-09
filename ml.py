from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers
import numpy as np

def resultSearch(teamName, matchList):
    results = []
    matchesFound = []
    
    for x in range(len(matchList)):
        if matchList[x].teamOne == teamName:
            matchesFound.append(matchList[x])
        if matchList[x].teamTwo == teamName:
            matchesFound.append(matchList[x])

    for y in range(len(matchesFound)):
        
        if str(matchesFound[y].winner) == str(teamName):
            results.append(1)
        elif str(matchesFound[y].winner) == "Draw":
            results.append(0.5)
        else:
            results.append(0)
        
    return(results)
                   
                
def encode(teamList):
    print("encoding")
    for x in range(len(teamList)):
        teamList[x].possession = (teamList[x].possession/teamList[x].matchesPlayed) / 100
        teamList[x].shots = (teamList[x].shots /teamList[x].matchesPlayed) / 10
        teamList[x].onTarget = (teamList[x].onTarget /teamList[x].matchesPlayed) /10
        teamList[x].offTarget = (teamList[x].offTarget / teamList[x].matchesPlayed) / 10
        teamList[x].goalD = (teamList[x].goalsFor - teamList[x].goalsAgainst) / 10


def create_model():
	# creates model layers
	model = Sequential()
	model.add(Dense(12, input_dim=5, activation='tanh'))
	model.add(Dense(12, activation='tanh'))
	model.add(Dense(8, activation='tanh'))
	model.add(Dense(1, activation='sigmoid'))
	model.compile(loss='binary_crossentropy', optimizer='adam')
	return model

    


        
    

        



                            
                
            
        
                   
