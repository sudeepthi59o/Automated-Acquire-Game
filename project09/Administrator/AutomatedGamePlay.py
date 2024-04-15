from Game import Game
import random
from GameTree import GameTreeAdmin
from GameTree import GameTreePlayer

class AutomatedGamePlay:
    def __init__(self,state=None,test_mode=None) -> None:
        self.game=Game(state)
        self.game.mode='automated'
        self.hotels=list(self.game.board.allHotels.keys())


    def setupGame(self):
        self.p1_strategy=1
        self.p2_strategy=2
        self.p3_strategy=3
        self.p4_strategy=4
        #Pick a strategy for the game: 1 - Ordered, 2 - Random, 3 - Alphabetical, 4- Anti Alphabetical 
        self.game.setup(players=["Player1","Player2","Player3","Player4"],strategies=[self.p1_strategy,self.p2_strategy,self.p3_strategy,self.p4_strategy])
    
    def nextTurn(self):
        self.game.board.printB()
        print("Turn Over")
        print("=============================================================>")
        
        if self.game.players[0].strategy==1:
            return self.orderedStrategy()
        elif self.game.players[0].strategy==2:
            return self.randomStrategy()
        elif self.game.players[0].strategy==3:
            return self.alphabeticalStrategy()
        elif self.game.players[0].strategy == 4:
            return self.anti_alphabeticalStrategy()
        
    def printCurrentStateOfPlayer(self):
        print("Player playing: "+self.game.players[0].name)
        print("Current state of players:")
        for i in range(len(self.game.players)):
            print(str(self.game.players[i]))
    

    def strategy(self,strategy):
        self.printCurrentStateOfPlayer()
        gtree=GameTreeAdmin(self.game)
        if gtree.isGameDone():
            print("=============================================================>")
            return "Game Ended! "+self.game.declare_winner()+" wins the game!!"
        children=gtree.generate()
        gplayer=GameTreePlayer(children)
        tile,to_buy,replace_tile,hotel=gplayer.pickChild(strategy=strategy,children=children)
        self.game.place(tile.row,tile.column,hotel)
        print("Tile placed: ",tile)
        for hotel in to_buy:
            res=self.game.buy(hotel)
            if res:
                print("Bought share in : ",hotel)
        print("Replacement tile: ",replace_tile)
        self.game.done(replace_tile)  

        return self.nextTurn()

    def orderedStrategy(self):
        return self.strategy("ordered")

    def alphabeticalStrategy(self):
        return self.strategy("largest-alpha")

    def anti_alphabeticalStrategy(self):
        return self.strategy("smallest-anti")
    
    def randomStrategy(self):
        return self.strategy("random")

    def playGame(self):
        self.setupGame()
        if self.p1_strategy==1:
            print(self.orderedStrategy())
        elif self.p1_strategy == 2:
            print(self.randomStrategy())
        elif self.p1_strategy== 3:
            print(self.alphabeticalStrategy())
        elif self.p1_strategy == 4:
            print(self.anti_alphabeticalStrategy())

g=AutomatedGamePlay()
g.playGame()
