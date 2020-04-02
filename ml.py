from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers
import numpy as np

def resultSearch(teamName, matchList):
    result = 0
    matchFound = []
    
    for x in range(len(matchList)):
        if matchList[x].teamOne == teamName:
            matchFound = matchList[x]
        if matchList[x].teamTwo == teamName:
            matchFound = matchList[x]

    print(matchFound.winner)

    if str(matchFound.winner) == str(teamName):
        result = 1
    elif str(matchFound.winner) == "Draw":
        result = 0
    else:
        result = -1
        
    return(result)
                   
                   

def encode(teamList):
    print("encoding")
    for x in range(len(teamList)):
        teamList[x].possession = (teamList[x].possession/teamList[x].matchesPlayed) / 100
        teamList[x].shots = (teamList[x].shots /teamList[x].matchesPlayed) / 100
        teamList[x].onTarget = (teamList[x].onTarget /teamList[x].matchesPlayed) /100
        teamList[x].offTarget = (teamList[x].offTarget / teamList[x].matchesPlayed) / 100
        teamList[x].goalD = (teamList[x].goalsFor - teamList[x].goalsAgainst) / 100 

def buildInputArray(teamList):
    tempInArray = np.zeros((20,5))

    for y in range(len(teamList)):
        tempInArray[y][0] = teamList[y].possession
        tempInArray[y][1] = teamList[y].shots
        tempInArray[y][2] = teamList[y].onTarget
        tempInArray[y][3] = teamList[y].offTarget
        tempInArray[y][4] = teamList[y].goalD

    return(tempInArray)
        
def buildOutputArray(teamList):
    tempOutputArray = np.zeros((20,1))

    for y in range(len(teamList)):
        tempOutputArray[y][0] = teamList[y].winPCT

    return(tempOutputArray)

def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(8, input_dim=5, activation='tanh'))
	model.add(Dense(1, activation='tanh'))
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

    


        
    

        



                            
                
            
        
                   
