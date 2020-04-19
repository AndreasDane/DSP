import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from ml import *
from teams import *
import csv
import random


##################### loading #####################

# Initialize variables
countries = ['Austria', 'Belgium', 'Croatia', 'Czech Republic', 'England', 'Germany', 'Hungary', 'Iceland', 'Italy', 'Northern Ireland', 'Poland', 'Portugal', 'Republic of Ireland', 'Russia', 'Slovakia', 'Spain', 'Sweden', 'Turkey', 'Ukraine', 'Wales']
groupID = ['B', 'C', 'D', 'E', 'F']

# unsorted team and match lists
teamList = []
matchList = []

# sorted team and match lists
trainList = []
testList = []
trainMatches = []
testMatches = []



# Function to sort a column by number value
def treeview_sort_column_int(treeview, col, reverse):
    tempList = [(treeview.set(item, col), item) for item in treeview.get_children('')] # creates copy of the column
    tempList.sort(key=lambda t: int(t[0]), reverse=reverse) # sorts column by int

    for index, (val, item) in enumerate(tempList): # numbers sorted column
        treeview.move(item, '', index) # moves column in treeview 

    treeview.heading(col, command=lambda: treeview_sort_column_int(treeview, col, not reverse))

def treeview_sort_column_float(treeview, col, reverse):
    tempList = [(treeview.set(item, col), item) for item in treeview.get_children('')] # creates copy of the column
    tempList.sort(key=lambda t: float(t[0]), reverse=reverse) # sorts column by float

    for index, (val, item) in enumerate(tempList): # nnumbers sorted column
        treeview.move(item, '', index) # moves column in treeview

    treeview.heading(col, command=lambda: treeview_sort_column_float(treeview, col, not reverse))

def treeview_sort_column_str(treeview, col, reverse):
    tempList = [(treeview.set(item, col), item) for item in treeview.get_children('')] # creates copy of the column
    tempList.sort(reverse=reverse) # sorts column alphabetically

    for index, (val, item) in enumerate(tempList): # nnumbers sorted column
        treeview.move(item, '', index) # moves column in treeview

    treeview.heading(col, command=lambda: treeview_sort_column_str(treeview, col, not reverse))


# Function to initialize team objects and assign attributes from CSV. 
def loadTeams():

    # clear table
    for i in rankView.get_children():
        rankView.delete(i)

    # clear stored teams
    teamList.clear()

    # create a team object for each country
    for x in countries:
        teamList.append(team(x))

    
    
    for x in range(len(countries)):
        with open('Team Data\\' + countries[x] + '.csv', "r") as csvfile:
            reader = csv.reader(csvfile)
            row = 1

            count = 0

            # assign statistics to team from csv
            for row in reader:
                for column in reader:
                    count += 1

                    teamList[x].possession += int(column[2])
                    teamList[x].onTarget += int(column[4])
                    teamList[x].offTarget += int(column[5])
                    teamList[x].goalsFor += int(column[6])
                    teamList[x].goalsAgainst += int(column[7])
        
                    print(column[1], column[2], column[3], column[4], column[5], column[6], column[7])


            teamList[x].matchesPlayed = count
            

            
            # insert team into GUI table
        
            #print(rankID)

    loadRanks()

    
# Function to load matches from CSV and initialize objects and assign attributes from CSV.
def loadMatches():

    # clear GUI match table
    for i in predictView.get_children():
        predictView.delete(i)

    # clear total stored matches
    matchList.clear()

    with open('Match Data\\matches.csv', "r") as csvfile:
        reader = csv.reader(csvfile)

        row = 1
        
        for row in reader:
            for column in reader:
                
                # create match objects and insert to GUI table                 
                matchID = predictView.insert('', 'end', values=(column[0], column[1], column[2] , 0, column[3]))
                print(matchID)
                matchList.append(match(str(column[0]), column[1], column[2], column[3], matchID))

                print(column[0], column[1], column[2], column[3])

    
def loadRanks():

        with open('Team Data\\teamconfig.csv', "r") as csvfile:

            reader = csv.reader(csvfile)

            row = 0
            x = 0
            
            for row in reader:
                   for column in reader:
                       print(column[1], column[2])
                       teamList[x].euroRank = int(column[1])
                       teamList[x].fifaRank = int(column[2])
                       teamList[x].group = str(column[3])
                       x += 1

            for y in range(len(teamList)):
                rankID = rankView.insert('', 'end', iid = teamList[y].name, values=(0, teamList[y].euroRank, teamList[y].fifaRank, teamList[y].name, teamList[y].group, 0))
            



# Function to sort teams for training and testing. 
def sortTeams(teamList, testGroup):

    trainList.clear()
    testList.clear()
    
    for x in range(len(teamList)):
        if str(teamList[x].group) == str(testGroup):
            testList.append(teamList[x])
        else:
            trainList.append(teamList[x])

# Function to sort matches for training and testing.
def sortMatches(matchList, testGroup):

    trainMatches.clear()
    testMatches.clear()

    for x in range(len(matchList)):
        if str(matchList[x].group) == str(testGroup):
            testMatches.append(matchList[x])
        else:
            trainMatches.append(matchList[x])


# Function to edit training/testing settings.
def ViewSettingsPrompt():
    
    settings = tk.Toplevel(mainMenu)

    modelLayersLabel = tk.Label(settings, text = "Number of layers in model: " + str(len(model.layers)))
 
    modelLayersLabel.pack(anchor = N)

    for x in range(len(model.layers)):
        label1 = tk.Label(settings, text= "Weights of Layer " + str(x+1) + ":" + str(model.layers[x].get_weights()[0])) # weights
        label2 = tk.Label(settings, text= "Bias of Layer " + str(x+1) + ":" + str(model.layers[x].get_weights()[1])) # bias
        label1.pack(anchor=N)
        label2.pack(anchor=N)

def helpPrompt():
    helpInfo = tk.Toplevel(mainMenu)
    
    trainingHelp = tk.Label(helpInfo, text = "\nTraining Help \n 1. Load BOTH team and match data. \n2. Select Encode button to encode previous match statistics for each team. \n3. Then select Training button. \n4. Once completed, the rank and match window will be updated to reflect the randomly selected teams and their matches used in training the model.")
    testingHelp = tk.Label(helpInfo, text = "\nTesting Help \n 1. After training has been performed. Select Testing button. \n3. Once testing is completed, the rank and match window will be updated to reflect the randomly selected test group and their matches.")
    fifaRankingHelp = tk.Label(helpInfo, text = "\nFIFA Ranking Help \n1. Load BOTH team and match data. \n2. Select Simulate with FIFA button. \n3. Once completed, the match window will display a predicted winner based on the June 2016 FIFA Rankings.")
    generateHelp = tk.Label(helpInfo, text = "\nGenerate Ranking Help \n1. AFTER a model has been trained following the steps listed in Training Help, select the Generate button. \n2. The rank and match menu will update to display ALL teams and matches after they have all been ran through the trained model.")

    trainingHelp.pack(anchor=N)
    testingHelp.pack(anchor=N)
    fifaRankingHelp.pack(anchor=N)
    generateHelp.pack(anchor=N)

# creates new random split of data
def initializeTraining():
    testGroup = random.choice(groupID)

    sortTeams(teamList, testGroup)
    sortMatches(matchList, testGroup)
    

        
    
##################### Main Menu GUI #####################
mainMenu = Tk()
mainMenu.title("Main Menu")
mainMenu.resizable(False, False)

menubar = Menu(mainMenu)
mainMenu.config(menu=menubar)

fileMenu = Menu(menubar)
fileMenu.add_command(label="Exit", command=quit)
menubar.add_cascade(label="File", menu=fileMenu)

helpMenu = Menu(menubar)
helpMenu.add_command(label="Help", command=helpPrompt)
menubar.add_cascade(label="Help", menu=helpMenu)


# Button Creations
loadTeamsBt = Button(mainMenu, text = "Load Team Data", command = loadTeams)
loadMatchesBt = Button(mainMenu, text = "Load Matches", command = loadMatches) 
trainingBt = Button(mainMenu, text = "Training", command = lambda: [ initializeTraining(), training(trainList, trainMatches, rankView, predictView, predictLabel)])
testingBt = Button(mainMenu, text = "Testing", command = lambda: testing(testList, testMatches, rankView, predictView, predictLabel))
encodeBt = Button(mainMenu, text = "Encode", command= lambda: encode(teamList))
editSettingsBt = Button(mainMenu, text="Settings", command = ViewSettingsPrompt)
generateBt = Button(mainMenu, text="Generate", command = lambda: generate(teamList, matchList, rankView, predictView, predictLabel))
simFifaBt = Button(mainMenu, text="Simulate with FIFA", command = lambda: simFIFAMatches(teamList, matchList, predictView, predictLabel))


# Button Placement
loadTeamsBt.grid(row = 2, column = 0, pady = 50, padx = 2, sticky = N)
loadMatchesBt.grid(row = 2, column = 0, pady = 50, padx = 2, sticky = S)    
editSettingsBt.grid(row = 3, column = 0, pady=50, padx=2, sticky = N)
encodeBt.grid(row = 3, column = 0, pady = 50, padx = 2, sticky = S)
trainingBt.grid(row = 4, column = 0, pady = 50, padx = 2, sticky = N)
testingBt.grid(row = 4, column = 0, pady = 50, padx = 2, sticky = S)

generateBt.grid(row = 4, column=2, pady=50,padx=2, sticky = S)
simFifaBt.grid(row=4, column=2, pady=50,padx=2, sticky=N)


# Rank Table
columns = ('Network Rank', 'EURO Rank', 'FIFA Rank', 'Team Name', 'Group', 'Rank Score')
rankView = Treeview(mainMenu, height = 20, columns=columns)


rankView['show'] = 'headings'
rankView.column("Network Rank", width=85, anchor=CENTER)
rankView.column("EURO Rank", width = 70, anchor=CENTER)
rankView.column("FIFA Rank", width=70, anchor=CENTER)
rankView.column("Team Name", width=400, anchor=CENTER)
rankView.column("Group", width=45, anchor=CENTER)
rankView.column("Rank Score", width=120)

rankView.heading("Network Rank",text="Network Rank", command=lambda : treeview_sort_column_int(rankView, "Network Rank", False))
rankView.heading("EURO Rank", text="EURO Rank", command = lambda: treeview_sort_column_int(rankView, "EURO Rank", False))
rankView.heading("FIFA Rank", text="FIFA Rank", command=lambda : treeview_sort_column_int(rankView, "FIFA Rank", False))
rankView.heading("Team Name", text="Team Name", command=lambda : treeview_sort_column_str(rankView, "Team Name", False))
rankView.heading("Group", text="Group", command=lambda : treeview_sort_column_str(rankView, "Group", False))
rankView.heading("Rank Score", text="Current Rank Score", command=lambda : treeview_sort_column_float(rankView, "Rank Score", False))



# Places rank table
rankView.grid(row = 2, column = 1, pady = 50, padx = 2, rowspan = 5)


##################### Prediction Menu GUI #####################
predictMenu = Tk()
predictMenu.title("Predictions Menu")
predictMenu.resizable(False, False)


# Prediction Widgets
predictLabel = Label(predictMenu, text="Predict Rate: ")

# Prediction Placement
predictLabel.grid(row=0,column =0, pady = 50, padx = 2)


yscrollbar = Scrollbar(predictMenu, orient='vertical')

# Prediction Table
predictColumns = ("Group", "Team One", "Team Two", "Predicted Result", "Real Result")

predictView = Treeview(predictMenu, height = 10, yscrollcommand = yscrollbar.set, columns=predictColumns)



predictView['show'] = 'headings'
predictView.column("Group", width=65, anchor=W)
predictView.column("Team One", width=150, minwidth=150, anchor=W)
predictView.column("Team Two", width=150, minwidth=150, anchor=W)
predictView.column("Predicted Result", width=150, minwidth=150, anchor=W)
predictView.column("Real Result", width=150, minwidth=150, anchor=W)

predictView.heading("Group", text="Group", command=lambda : treeview_sort_column_str(predictView, "Group", False))
predictView.heading("Team One",text="Team One", command=lambda : treeview_sort_column_str(predictView, "Team One", False))
predictView.heading("Team Two", text="Team Two", command=lambda : treeview_sort_column_str(predictView, "Team Two", False))
predictView.heading("Predicted Result", text="Predicted Result", command=lambda : treeview_sort_column_str(predictView, "Predicted Result", False))
predictView.heading("Real Result", text="Real Result", command=lambda : treeview_sort_column_str(predictView, "Real Result", False))


predictView.grid(row = 0, column = 1, pady = 50, padx = 2, rowspan = 4)
yscrollbar.grid(row=0, column=2, sticky='ns', rowspan = 4, pady = 50, padx = 2)
yscrollbar.configure(command=predictView.yview)





mainMenu.mainloop()
