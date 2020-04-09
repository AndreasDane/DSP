
from tkinter import *
from tkinter.ttk import *
from ml import *
from teams import *
import csv


##################### load #####################

countries = ['Austria', 'Belgium', 'Croatia', 'Czech Republic', 'England', 'Germany', 'Hungary', 'Iceland', 'Italy', 'Northern Ireland', 'Poland', 'Portugal', 'Republic of Ireland', 'Russia', 'Slovakia', 'Spain', 'Sweden', 'Turkey', 'Ukraine', 'Wales']
fifaRanks = [10, 2, 27, 30, 11, 4, 20, 34, 12, 25, 27, 8, 33, 29, 24, 6, 35, 18, 19, 26]
groupID = ['F','E','D','D','B','C','F','F','E','C','C','F', 'E', 'B', 'B', 'D', 'E', 'D', 'C', 'B']


teamList = []
matchList = []

trainList = []
testList = []
trainMatches = []
testMatches = []

trainInputs = np.zeros((16,5))
trainOutputs = np.zeros((16,1))


def loadTeams():
    for x in countries:
        teamList.append(team(x))
    
    for x in range(len(countries)):
        with open('Team Data\\' + countries[x] + '.csv', "r") as csvfile:
            reader = csv.reader(csvfile)
            row = 1

            wins = 0
            count = 0
            
            for row in reader:
                for column in reader:
                    count += 1

                    teamList[x].possession += int(column[2])
                    teamList[x].shots += int(column[3])
                    teamList[x].onTarget += int(column[4])
                    teamList[x].offTarget += int(column[5])
                    teamList[x].goalsFor += int(column[6])
                    teamList[x].goalsAgainst += int(column[7])
        
                    #if column[6] > column[7]:
                     #   wins += 1
                    #if column[6] == column[7]:
                     #   wins += 0.5
  
                    print(column[1], column[2], column[3], column[4], column[5], column[6], column[7])
                    #print(wins)

            teamList[x].matchesPlayed = count
            teamList[x].fifaRank = fifaRanks[x]
            teamList[x].group = groupID[x]
            #teamList[x].winPCT = wins/teamList[x].matchesPlayed
                    
            rankView.insert('', 'end', text=x, values=(teamList[x].fifaRank, teamList[x].name, ""))


    sortTeams(teamList)

def loadMatches():

    matchList.clear()

    with open('Match Data\\matches.csv', "r") as csvfile:
        reader = csv.reader(csvfile)

        row = 1
        
        for row in reader:
            for column in reader:
                matchList.append(match(str(column[0]), column[1], column[2], column[3]))
                                          
                print(column[0], column[1], column[2], column[3])

    sortMatches(matchList)


def sortTeams(teamList):
    for x in range(len(teamList)):
        if teamList[x].group == 'F':
            testList.append(teamList[x])
        else:
            trainList.append(teamList[x])

def sortMatches(matchList):
    for x in range(len(matchList)):
        if matchList[x].group == 'F':
            testMatches.append(matchList[x])
        else:
            trainMatches.append(matchList[x])
            
def simMatches(teamList, matches):
    total = len(matches)
    correct = 0
    perc = 0
    
    for x in range(len(trainMatches)):
        teamOne = 0
        teamTwo = 0
        predictedWinner = ''

        for y in range(len(teamList)):
            if teamList[y].name == trainMatches[x].teamOne:
                teamOne = teamList[y]
            if teamList[y].name == trainMatches[x].teamTwo:
                teamTwo = teamList[y]

        if abs((teamOne.rating) - (teamTwo.rating)) < 0.0001:
            predictedWinner = "Draw"
            #print("DRAW PREDICTED!")
        elif teamOne.rating > teamTwo.rating:
            predictedWinner = teamOne.name
            #print("PREDICTED WINNER: " + predictedWinner)
        else:
            predictedWinner = teamTwo.name
            #print("PREDICTED WINNER: " + predictedWinner)

        #print("REAL WINNER: " + trainMatches[x].winner)

        if predictedWinner == trainMatches[x].winner:
            correct += 1           
           

    perc = (correct / total)  *  100
    print(perc)

def simFIFAMatches(teamList, matches):
    total = len(matches)
    correct = 0
    perc = 0
    
    for x in range(len(trainMatches)):
        teamOne = 0
        teamTwo = 0
        predictedWinner = ''

        for y in range(len(teamList)):
            if teamList[y].name == trainMatches[x].teamOne:
                teamOne = teamList[y]
            if teamList[y].name == trainMatches[x].teamTwo:
                teamTwo = teamList[y]

        if abs((teamOne.fifaRank) - (teamTwo.fifaRank)) <= 2:
            predictedWinner = "Draw"
            print("DRAW PREDICTED!")
        elif teamOne.fifaRank < teamTwo.fifaRank:
            predictedWinner = teamOne.name
            print("PREDICTED WINNER: " + predictedWinner)
        else:
            predictedWinner = teamTwo.name
            print("PREDICTED WINNER: " + predictedWinner)

        print("REAL WINNER: " + trainMatches[x].winner)

        if predictedWinner == trainMatches[x].winner:
            correct += 1           
           

    perc = (correct / total)  *  100
    print(perc)


def training(trainList):

    model = create_model()

    for x in range(len(trainList)):
        trainList[x].form = resultSearch(trainList[x].name, matchList)

    for y in range(len(trainList)):
        trainInputs[y][0] = trainList[y].possession
        trainInputs[y][1] = trainList[y].shots
        trainInputs[y][2] = trainList[y].onTarget
        trainInputs[y][3] = trainList[y].offTarget
        trainInputs[y][4] = trainList[y].goalD


    for g in range(3):

        for i in range(len(trainList)):
            trainOutputs[i][0] = trainList[i].form[g]

        model.fit(trainInputs, trainOutputs, epochs = 100)


    ratings = model.predict(trainInputs)

    for n in range(len(trainList)):
        trainList[n].rating = ratings[n]
        

    print(ratings)
    simMatches(trainList, trainMatches)


    
##################### Main Menu GUI #####################
mainMenu = Tk()
mainMenu.title("Main Menu")
mainMenu.resizable(False, False)

# Button Creations
loadTeamsBt = Button(mainMenu, text = "Load Team Data", command = loadTeams)
loadMatchesBt = Button(mainMenu, text = "Load Matches", command = loadMatches) 
generateBt = Button(mainMenu, text = "Training", command = lambda: training(trainList))
encodeBt = Button(mainMenu, text = "Encode", command= lambda: encode(teamList))

# Button Placement
loadTeamsBt.grid(row = 2, column = 0, pady = 50, padx = 2, sticky = N)
loadMatchesBt.grid(row = 2, column = 0, pady = 50, padx = 2, sticky = S)
encodeBt.grid(row = 5, column = 0, pady = 50, padx = 2, sticky = N)
generateBt.grid(row = 5, column = 0, pady = 50, padx = 2, sticky = S)

# Rank Table
rankColumns = ('Network Rank', 'FIFA Rank', 'Team Name', 'Rank Score')
rankView = Treeview(mainMenu, height = 20, columns=rankColumns)

rankView['columns'] = ("one","two","three")
rankView.column("#0", width=55, minwidth=55, anchor=CENTER)
rankView.column("one", width=55, minwidth=55, anchor=CENTER)
rankView.column("two", width=400, minwidth=200)
rankView.column("three", width=80, minwidth=50)

rankView.heading("#0",text="Network \nRank")
rankView.heading("one", text="FIFA \nRank")
rankView.heading("two", text="Team Name")
rankView.heading("three", text="Rank Score")



rankView.grid(row = 2, column = 1, pady = 50, padx = 2, rowspan = 4)


##################### Prediction Menu GUI #####################
predictMenu = Tk()
predictMenu.title("Predictions Menu")
predictMenu.resizable(False, False)

# Prediction Widgets
predictRateLabel = Label(predictMenu, text="Predict Rate: \nX%")

# Prediction Placement
predictRateLabel.grid(row=0,column =0, pady = 50, padx = 2)


yscrollbar = Scrollbar(predictMenu, orient='vertical')

# Prediction Table
predictView = Treeview(predictMenu, height = 10, yscrollcommand = yscrollbar.set)
predictView['columns'] = ("one","two","three")
predictView.column("#0", width=150, minwidth=150, anchor=W)
predictView.column("one", width=150, minwidth=150, anchor=W)
predictView.column("two", width=150, minwidth=150, anchor=W)
predictView.column("three", width=150, minwidth=150, anchor=W)


predictView.heading("#0",text="Team One")
predictView.heading("one", text="Team Two")
predictView.heading("two", text="Predicted Result")
predictView.heading("three", text="Real Result")


predictView.grid(row = 0, column = 1, pady = 50, padx = 2, rowspan = 4)
yscrollbar.grid(row=0, column=2, sticky='ns', rowspan = 4, pady = 50, padx = 2)
yscrollbar.configure(command=predictView.yview)


# Table Insert
for x in range(60):
    predictView.insert('', 'end', text="Republic of Ireland " + str(x), values=("abc", "cde", "fgh"))


mainMenu.mainloop()
