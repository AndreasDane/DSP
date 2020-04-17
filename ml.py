from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers
from keras import backend as K 
import numpy as np
import tkinter.messagebox


# training and testing arrays
trainInputs = np.zeros((16,4))
trainOutputs = np.zeros((16,1))

testInputs = np.zeros((4,4))

completeInputs = np.zeros((20,4))

# Creates a neural network model
def create_model():
        
	# creates model layers
	model = Sequential()

	
	model.add(Dense(2, input_dim=4, activation='tanh'))
	model.add(Dense(1, activation='sigmoid'))
	
	model.compile(loss='binary_crossentropy', optimizer='adam')
	return model

model = create_model()

# function to assign rank to teams in a list based on rating score
def sortRatings(teamList):
        
        teamList.sort(key=lambda team: team.rating, reverse=True)

        for x in range(len(teamList)):
                teamList[x].networkRank = x+1
   

# Function to simulate matches based on the new rankings
def simMatches(teamList, matches, predictView):
    total = len(matches)
    correct = 0
    perc = 0
    
    for x in range(len(matches)):
        teamOne = 0
        teamTwo = 0
        predictedWinner = ''
        matchID = matches[x].matchID

        for y in range(len(teamList)):
            if teamList[y].name == matches[x].teamOne:
                teamOne = teamList[y]
            if teamList[y].name == matches[x].teamTwo:
                teamTwo = teamList[y]

        if abs((teamOne.rating) - (teamTwo.rating)) < 0.005:
            predictedWinner = "Draw"
            #print("DRAW PREDICTED!")
        elif teamOne.rating > teamTwo.rating:
            predictedWinner = teamOne.name
            #print("PREDICTED WINNER: " + predictedWinner)
        else:
            predictedWinner = teamTwo.name
            #print("PREDICTED WINNER: " + predictedWinner)

        predictView.set(matchID, 'Predicted Result', str(predictedWinner))

        #print("REAL WINNER: " + matches[x].winner)

        if predictedWinner == matches[x].winner:
            correct += 1           

           

    perc = (correct / total)  *  100
    return(perc)

# Function to simulate matches based on assigned FIFA Ranking
def simFIFAMatches(teamList, matches, predictView, predictLabel):
    total = len(matches)
    correct = 0
    perc = 0

    for m in predictView.get_children():
        predictView.delete(m)

    for l in range(len(matches)):
        predictView.insert('', 'end', iid=matches[l].matchID, values=(matches[l].group, matches[l].teamOne, matches[l].teamTwo , 0, matches[l].winner))


    # assembles results of teams for use in training outputs

    
    for x in range(len(matches)):
        teamOne = 0
        teamTwo = 0
        predictedWinner = ''

        for y in range(len(teamList)):
            if teamList[y].name == matches[x].teamOne:
                teamOne = teamList[y]
            if teamList[y].name == matches[x].teamTwo:
                teamTwo = teamList[y]

        if abs((teamOne.fifaRank) - (teamTwo.fifaRank)) <= 3:
            predictedWinner = "Draw"
            print("DRAW PREDICTED!")    
        elif teamOne.fifaRank < teamTwo.fifaRank:
            predictedWinner = teamOne.name
            print("PREDICTED WINNER: " + predictedWinner)
        else:
            predictedWinner = teamTwo.name
            print("PREDICTED WINNER: " + predictedWinner)

        print("REAL WINNER: " + matches[x].winner)

        predictView.set(matches[x].matchID, 'Predicted Result', str(predictedWinner))

        if str(predictedWinner) == str(matches[x].winner):
            correct += 1           

    
        
    perc = (correct / total)  *  100
    
    predictLabel.configure(text = "Predict Rate: " + str(perc) + "%")

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
                   
# Function to encode match statistics
def encode(teamList):
    print("encoding")
    for x in range(len(teamList)):
        teamList[x].possession = (teamList[x].possession/teamList[x].matchesPlayed) / 100
        teamList[x].onTarget = (teamList[x].onTarget /teamList[x].matchesPlayed) / 10
        teamList[x].offTarget = (teamList[x].offTarget / teamList[x].matchesPlayed) /10
        teamList[x].goalD = (teamList[x].goalsFor - teamList[x].goalsAgainst) / 10
    
# Function for training sequence 
def training(trainList, trainMatches, rankView, predictView, predictLabel):

    model

    accuracyperc = 0

    # clears all teams from GUI table
    for i in rankView.get_children():
        rankView.delete(i)

    for m in predictView.get_children():
        predictView.delete(m)

    # adds only teams/matches used in training to GUI table
    for t in range(len(trainList)):
            rankView.insert('', 'end', iid = trainList[t].name, text=0, values=(0, trainList[t].euroRank, trainList[t].fifaRank, trainList[t].name, trainList[t].group, 0))

    for l in range(len(trainMatches)):
            predictView.insert('', 'end', iid=trainMatches[l].matchID, text= trainMatches[l].teamOne, values=(trainMatches[l].group, trainMatches[l].teamOne, trainMatches[l].teamTwo , 0, trainMatches[l].winner))


    # assembles results of teams for use in training outputs
    for x in range(len(trainList)):
        trainList[x].form = resultSearch(trainList[x].name, trainMatches)

    # assigns training input vectors (match statistics) 
    for y in range(len(trainList)):
        trainInputs[y][0] = trainList[y].possession
        trainInputs[y][1] = trainList[y].onTarget
        trainInputs[y][2] = trainList[y].offTarget
        trainInputs[y][3] = trainList[y].goalD


    # assigns training outputs from previously searched results
    for g in range(3):

        for i in range(len(trainList)):
            trainOutputs[i][0] = trainList[i].form[g]

        model.fit(trainInputs, trainOutputs, epochs = 100)
        
    # displays ratings
    ratings = model.predict(trainInputs)

    # assigns ratings
    for n in range(len(trainList)):
        trainList[n].rating = ratings[n]

    sortRatings(trainList)

    for f in range(len(trainList)):
        rankView.set(str(trainList[f].name), 'Rank Score', float(trainList[f].rating))
        rankView.set(str(trainList[f].name), 'Network Rank', trainList[f].networkRank)
        

    print(ratings)

    # simulates matches to obtain prediction accuracy
    
    accuracyperc = simMatches(trainList, trainMatches, predictView)

    predictLabel.configure(text = "Predict Rate: " + str(accuracyperc) + "%")
    
def testing(testList, testMatches, rankView, predictView, predictLabel):

    # clears all teams from GUI table
    for i in rankView.get_children():
        rankView.delete(i)

    for m in predictView.get_children():
        predictView.delete(m)

    # adds teams and matches in testing process to GUI table
    for t in range(len(testList)):
            rankView.insert('', 'end', iid = testList[t].name, values=(0, testList[t].euroRank, testList[t].fifaRank, testList[t].name, testList[t].group, 0))

    for l in range(len(testMatches)):
            predictView.insert('', 'end', iid=testMatches[l].matchID,  values=(testMatches[l].group, testMatches[l].teamOne, testMatches[l].teamTwo , 0, testMatches[l].winner))

    # assigns testing input vectors (match statistics) 
    for y in range(len(testList)):
        testInputs[y][0] = testList[y].possession
        testInputs[y][1] = testList[y].onTarget
        testInputs[y][2] = testList[y].offTarget
        testInputs[y][3] = testList[y].goalD


    # displays ratings
    ratings = model.predict(testInputs)

    # assigns ratings
    for n in range(len(testList)):
        testList[n].rating = ratings[n]

    sortRatings(testList)

    for f in range(len(testList)):
        rankView.set(str(testList[f].name), 'Rank Score', float(testList[f].rating))
        rankView.set(str(testList[f].name), 'Network Rank', testList[f].networkRank)
        

    print(ratings)

    # simulates matches to obtain prediction accuracy
    try:
        accuracyperc = simMatches(testList, testMatches, predictView)
    except ZeroDivisionError:
        tkinter.messagebox.showinfo('Error:', 'Cannot perform rank generation until teams and matches are loaded.')
                    
    predictLabel.configure(text = "Predict Rate: " + str(accuracyperc) + "%")
    
def generate(teamList, matchList, rankView, predictView, predictLabel):

    # clear GUI tables for matches and teams
    for i in rankView.get_children():
        rankView.delete(i)

    for m in predictView.get_children():
        predictView.delete(m)

    # insert teams used into GUI table
    for t in range(len(teamList)):
            rankView.insert('', 'end', iid = teamList[t].name, values=(0, teamList[t].euroRank, teamList[t].fifaRank, teamList[t].name, teamList[t].group, 0))

    for l in range(len(matchList)):
            predictView.insert('', 'end', iid=matchList[l].matchID,  values=(matchList[l].group, matchList[l].teamOne, matchList[l].teamTwo , 0, matchList[l].winner))

    # assigns testing input vectors (match statistics) 
    for y in range(len(teamList)):
        completeInputs[y][0] = teamList[y].possession
        completeInputs[y][1] = teamList[y].onTarget
        completeInputs[y][2] = teamList[y].offTarget
        completeInputs[y][3] = teamList[y].goalD


    # displays ratings
    ratings = model.predict(completeInputs)

    # assigns ratings
    for n in range(len(teamList)):
        teamList[n].rating = ratings[n]

    sortRatings(teamList)


    for f in range(len(teamList)):
        rankView.set(str(teamList[f].name), 'Rank Score', float(teamList[f].rating))
        rankView.set(str(teamList[f].name), 'Network Rank', teamList[f].networkRank)
        

    print(ratings)

    # simulates matches to obtain prediction accuracy
    try:
            accuracyperc = simMatches(teamList, matchList, predictView)
    except ZeroDivisionError:
            tkinter.messagebox.showinfo('Error:', 'Cannot perform rank generation until teams and matches are loaded.')
            
    predictLabel.configure(text = "Predict Rate: " + str(accuracyperc) + "%")
    


