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
fifaRanks = [10, 2, 27, 30, 11, 4, 20, 34, 12, 25, 27, 8, 33, 29, 24, 6, 35, 18, 19, 26]
groupID = ['F','E','D','D','B','C','F','F','E','C','C','F', 'E', 'B', 'B', 'D', 'E', 'D', 'C', 'B']

# unsorted team and match lists
teamList = []
matchList = []

# sorted team and match lists
trainList = []
testList = []
trainMatches = []
testMatches = []

# https://tekrecipes.com/2019/04/20/tkinter-treeview-enable-sorting-upon-clicking-column-headings/
# Function to sort a column by number value
def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')] # creates copy of the column
    l.sort(key=lambda t: int(t[0]), reverse=reverse) # sorts column by int

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))


# Function to initialize team objects and assign attributes from CSV. 
def loadTeams():

    for i in rankView.get_children():
        rankView.delete(i)

    teamList.clear()
    
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

            rankID = rankView.insert('', 'end', iid = teamList[x].name, values=(0, teamList[x].fifaRank, teamList[x].name, 0))
            print(rankID)

    sortTeams(teamList)

# Function to load matches from CSV and initialize objects and assign attributes from CSV.
def loadMatches():

    for i in predictView.get_children():
        predictView.delete(i)

    matchList.clear()

    with open('Match Data\\matches.csv', "r") as csvfile:
        reader = csv.reader(csvfile)

        row = 1
        
        for row in reader:
            for column in reader:
                
                                          
                matchID = predictView.insert('', 'end', values=(column[1], column[2] , 0, column[3]))
                print(matchID)
                matchList.append(match(str(column[0]), column[1], column[2], column[3], matchID))

                print(column[0], column[1], column[2], column[3])

    sortMatches(matchList)

# Function to sort teams for training and testing. 
def sortTeams(teamList):
    for x in range(len(teamList)):
        if str(teamList[x].group) == testGroup.get():
            testList.append(teamList[x])
        else:
            trainList.append(teamList[x])

# Function to sort matches for training and testing.
def sortMatches(matchList):
    for x in range(len(matchList)):
        if str(matchList[x].group) == testGroup.get():
            testMatches.append(matchList[x])
        else:
            trainMatches.append(matchList[x])


# Function to edit training/testing settings.
def ViewSettingsPrompt():
    settings = tk.Toplevel(mainMenu)


    instructionLabel = tk.Label(settings, text = "The current testing group: " + str(testGroup.get()))

    instructionLabel.pack(anchor = N)

    

def helpPrompt():
    helpInfo = tk.Toplevel(mainMenu)

    helpLabel = tk.Label(helpInfo, text = "Help")


    

    
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

testGroup = tk.StringVar()
testGroup.set(random.choice(groupID))

# Button Creations
loadTeamsBt = Button(mainMenu, text = "Load Team Data", command = loadTeams)
loadMatchesBt = Button(mainMenu, text = "Load Matches", command = loadMatches) 
trainingBt = Button(mainMenu, text = "Training", command = lambda: training(trainList, trainMatches, rankView, predictView, predictLabel))
testingBt = Button(mainMenu, text = "Testing", command = lambda: testing(testList, testMatches, rankView, predictView, predictLabel))
encodeBt = Button(mainMenu, text = "Encode", command= lambda: encode(teamList))
editSettingsBt = Button(mainMenu, text="Settings", command = ViewSettingsPrompt)
generateBt = Button(mainMenu, text="Generate", command = lambda: generate(teamList, matchList, rankView, predictView, predictLabel))

# Button Placement
loadTeamsBt.grid(row = 2, column = 0, pady = 50, padx = 2, sticky = N)
loadMatchesBt.grid(row = 2, column = 0, pady = 50, padx = 2, sticky = S)
editSettingsBt.grid(row = 3, column = 0, pady=50, padx=2, sticky = N)
encodeBt.grid(row = 3, column = 0, pady = 50, padx = 2, sticky = S)
trainingBt.grid(row = 4, column = 0, pady = 50, padx = 2, sticky = N)
testingBt.grid(row = 4, column = 0, pady = 50, padx = 2, sticky = S)
generateBt.grid(row = 4, column=2, pady=50,padx=2, sticky = S)



# Rank Table
columns = ('Network Rank', 'FIFA Rank', 'Team Name', 'Rank Score')
rankView = Treeview(mainMenu, height = 20, columns=columns)

rankView['show'] = 'headings'
rankView.column("Network Rank", width=65, minwidth=55, anchor=CENTER)
rankView.column("FIFA Rank", width=65, minwidth=55, anchor=CENTER)
rankView.column("Team Name", width=400, minwidth=200)
rankView.column("Rank Score", width=120, minwidth=50)

rankView.heading("Network Rank",text="Network \nRank", command=lambda : treeview_sort_column(rankView, "Network Rank", False))
rankView.heading("FIFA Rank", text="FIFA \nRank", command=lambda : treeview_sort_column(rankView, "FIFA Rank", False))
rankView.heading("Team Name", text="Team Name")
rankView.heading("Rank Score", text="Current Rank Score", command=lambda : treeview_sort_column(rankView, "Rank Score", False))



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
predictColumns = ("Team One", "Team Two", "Predicted Result", "Real Result")

predictView = Treeview(predictMenu, height = 10, yscrollcommand = yscrollbar.set, columns=predictColumns)



predictView['show'] = 'headings'
predictView.column("Team One", width=150, minwidth=150, anchor=W)
predictView.column("Team Two", width=150, minwidth=150, anchor=W)
predictView.column("Predicted Result", width=150, minwidth=150, anchor=W)
predictView.column("Real Result", width=150, minwidth=150, anchor=W)


predictView.heading("Team One",text="Team One")
predictView.heading("Team Two", text="Team Two")
predictView.heading("Predicted Result", text="Predicted Result")
predictView.heading("Real Result", text="Real Result")


predictView.grid(row = 0, column = 1, pady = 50, padx = 2, rowspan = 4)
yscrollbar.grid(row=0, column=2, sticky='ns', rowspan = 4, pady = 50, padx = 2)
yscrollbar.configure(command=predictView.yview)





mainMenu.mainloop()
