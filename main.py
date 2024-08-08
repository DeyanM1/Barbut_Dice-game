import random
import sys
import time

import numpy as np

from rich import print as richPrint
from rich.console import Console
from rich.table import Table
from rich import pretty

pretty.install()

console = Console()

def checkSameElements(lst):
    lst.sort()
    return len(set(lst)) == 1

def testValid(lst):
    validNums = [1, 5]
    for elem in lst:
        if elem in validNums:
            return True
    
    return False

ROAD_DICES = [[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]

class Player:
    def __init__(self, name):
        self.dice = [0, 0, 0]
        self.name = name
        self.points = 0
        self.pointsToAdd = 0
        self.place = None
        
        self.rerollAll = False
        
        self.roll([0, 1, 2])
        
    def roll(self, idList: list):
        for id in idList:
            if id not in range(0, 3):
                raise ValueError(f"Invalid dice Value: {id}")
            #self.dice[id] = secrets.randbelow(6) + 1
            self.dice[id] = np.random.randint(1, 7, size=1).item()
    
    def move(self):
        self.roll((0, 1, 2))
        self.rerollAll = True
        canReroll, rerollIdList= self.identify((0, 1, 2))
        
        if canReroll == False:
            richPrint(f"[purple][{self.name}][/purple] rolled: {self.dice} No valid nums - 0p  |  [magenta]{self.points}p[/magenta]")
        else:
            richPrint(f"[purple][{self.name}][/purple] rolled: {self.dice} - [magenta]{self.pointsToAdd}p[/magenta]  |  [magenta]{self.points}p[/magenta]")
            select = input("Enter 0 to write the points, enter 1 to reroll the dice -> ")
        
            if select == "0":
                self.points += self.pointsToAdd
                self.pointsToAdd = 0
            else:
                self.roll(rerollIdList)
                testDice = []
                for id in rerollIdList:
                    testDice.append(self.dice[id])
                    
                if testValid(testDice) == False:
                    richPrint(f"[purple][{self.name}][/purple] rolled: {self.dice} No valid nums - [magenta]0p[/magenta]  |  [magenta]{self.points}p[/magenta]")
                    self.pointsToAdd = 0
                    canReroll = False

                
                while canReroll == True and select == "1":
                    canReroll, rerollIdList= self.identify(rerollIdList)
                    if canReroll == False:
                        print(f"[purple][{self.name}][/purple] rolled: {self.dice} - [magenta]{self.pointsToAdd}p[/magenta]  |  [magenta]{self.points}p[/magenta]")
                    else:
                        print(f"[purple][{self.name}][/purple] rolled: {self.dice} - [magenta]{self.pointsToAdd}p[/magenta]  |  [magenta]{self.points}p[/magenta]")
                        select = input("Enter 0 to write the points, enter 1 to reroll the dice -> ")
                    
                        if select == "0":
                            self.points += self.pointsToAdd
                            self.pointsToAdd = 0
                        elif select == "1":
                            self.roll(rerollIdList)
                            print(rerollIdList)
                            testDice = []
                            for id in rerollIdList:
                                testDice.append(self.dice[id])
                                
                            if testValid(testDice) == False:
                                print(f"[purple][{self.name}][/purple] rolled: {self.dice} No valid nums - [magenta]0p[/magenta]  |  [magenta]{self.points}p[/magenta]")
                                self.pointsToAdd = 0
                                canReroll = False
        
        
    def identify(self, idListToIdentify: list):
        noRerollIdList = []
        rerollIdList = []
        

        if checkSameElements(self.dice) and self.rerollAll == True:
            match self.dice[0]:
                case 1: self.pointsToAdd += 1000
                case 2: self.pointsToAdd += 200
                case 3: self.pointsToAdd += 300
                case 4: self.pointsToAdd += 400
                case 5: self.pointsToAdd += 500
                case 6: self.points = 0
            
            rerollIdList = [0, 1, 2]    
            return True, rerollIdList
        elif self.dice in ROAD_DICES:
            self.pointsToAdd += 200
            
            rerollIdList = [0, 1, 2]    
            return True, rerollIdList
        
        for id in idListToIdentify:
            if id not in range(0, 3):
                raise ValueError(f"Invalid dice Value: {id}")
            
            match self.dice[id]:
                case 1: self.pointsToAdd += 100; noRerollIdList.append(id)
                case 2: self.pointsToAdd += 0; rerollIdList.append(id)
                case 3: self.pointsToAdd += 0; rerollIdList.append(id)
                case 4: self.pointsToAdd += 0; rerollIdList.append(id)
                case 5: self.pointsToAdd += 50; noRerollIdList.append(id)
                case 6: self.pointsToAdd += 0; rerollIdList.append(id)
        
        
        if len(noRerollIdList) == 3:
            noRerollIdList = []
            rerollIdList = [0, 1, 2]
            self.rerollAll = True
            return True, rerollIdList
        
        elif len(rerollIdList) == 3:
            return False, rerollIdList
        else:
            self.rerollAll = False
            return True, rerollIdList
    




def displayScore(players:list):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Player", style="cyan", justify="left")
    table.add_column("Score", style="magenta", justify="center")

    for player in players:
        table.add_row(f"{player.name}", str(player.points))
        
    console.print(table)

def displayFinalScore(players:list):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Player", style="cyan", justify="left")
    table.add_column("Score", style="magenta", justify="center")
    table.add_column("Place", style="yellow", justify="center")

    for player in players:
        table.add_row(f"{player.name}", str(player.points), str(player.place))
        
    console.print(table)



places = ["1st 👑", "2nd 🥈", "3rd 🥉", "4th", "5th", "6th", "7th", "8th", "9th", "10th"]

######### Play ########
if __name__ == '__main__':   
    richPrint("Enter the [bold magenta]Player count[/bold magenta] -> ", end="")
    playerCount = int(input())
    richPrint("Enter amount of [bold magenta]points to win[/bold magenta] -> ", end="")
    finishPoints = int(input())
    
    
    players = []
    
    for _ in range(playerCount):
        richPrint(f"Enter [bold magenta]Player {_+1}'s[/bold magenta] name -> ", end="")
        name = input()
        players.append(Player(name))

    
    
    round = 1
    
    richPrint("------- [green]Game Start[/green] -------")
    
    
    
    while True:
        richPrint(f"-------- Round: {round} --------")
        displayScore(players)
        
        for currentPlayer in players:
            currentPlayer.move()
            
            if currentPlayer.points > finishPoints:
                richPrint(f"######## [purple][{currentPlayer.name}][/purple] won the game with [magenta]{currentPlayer.points}p[/magenta] in [magenta]{round}p[/magenta] ########")
                winners = players.sort(key = lambda player: player.points, reverse=True)
                
                for player in range(len(players)):
                    players[player].place = places[player]
                    
                displayFinalScore(players)
                quit()              
                                                  
            time.sleep(1) 
        
        time.sleep(2)
        
        round += 1