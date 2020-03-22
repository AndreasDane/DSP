import csv
from tkinter import *
from tkinter.ttk import *
from teams import *

##################### load #####################

countries = ['Austria', 'Belgium', 'Croatia', 'Czech Republic', 'England', 'Germany', 'Hungary', 'Iceland', 'Italy', 'Northern Ireland', 'Poland', 'Portugal', 'Republic of Ireland', 'Russia', 'Slovakia', 'Spain', 'Sweden', 'Turkey', 'Ukraine', 'Wales']
fifaRanks = [10, 2, 27, 30, 11, 4, 20, 34, 12, 25, 27, 8, 33, 29, 24, 6, 35, 18, 19, 26]

teamList = []

def load():
    for x in countries:
        teamList.append(team(x))
    
    for x in range(len(countries)):
        with open('Team Data\\' + countries[x] + '.csv', "r") as csvfile:
            reader = csv.reader(csvfile)
            row = 1

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
        
                    
                    print(column[1], column[2], column[3], column[4], column[5], column[6], column[7])

            teamList[x].matchesPlayed = count
            teamList[x].fifaRank = fifaRanks[x]
            rankView.insert('', 'end', text=x, values=(teamList[x].fifaRank, teamList[x].name, ""))

### Insertion sort ###

            
##################### Main Menu GUI #####################
mainMenu = Tk()
mainMenu.title("Main Menu")
mainMenu.resizable(False, False)

# Button Creations
loadTeamsBt = Button(mainMenu, text = "Load Team Data", command = load)
loadTrainBt = Button(mainMenu, text = "Load Training Matches") 
loadTestBt = Button(mainMenu, text = "Load Test Matches")
generateBt = Button(mainMenu, text = "Generate Ranking")
encodeBt = Button(mainMenu, text = "Encode")

# Button Placement
loadTeamsBt.grid(row = 2, column = 0, pady = 50, padx = 2, sticky = N)
loadTrainBt.grid(row = 2, column = 0, pady = 50, padx = 2)
loadTestBt.grid(row = 2, column = 0, pady = 50, padx = 2, sticky = S)
encodeBt.grid(row = 5, column = 0, pady = 50, padx = 2, sticky = N)
generateBt.grid(row = 5, column = 0, pady = 50, padx = 2, sticky = S)

# Rank Table
rankView = Treeview(mainMenu, height = 20)
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





predictMenu.mainloop()
mainMenu.mainloop()
