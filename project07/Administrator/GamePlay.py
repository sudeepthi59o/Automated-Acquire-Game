from Game import Game
from AutomatedPlayer import AutomatedPlayer

class GamePlay:
    def __init__(self) -> None:
        self.game=Game()
        self.game.mode='automated'
        
    def setupGame(self):
        self.p1_strategy=1
        #int(input('Pick a strategy for the game: 1 - Ordered, 2 - Random ---->'))  #Add validation for input
        self.p2_strategy=self.p1_strategy      #Assigning same strategy to both players
        self.game.setup(["Player A","Player B"],self.p1_strategy)
        #self.game.board.printB()

    def minTile(self,minRow,minCol):
        smallestRow=minRow
        smallestCol=minCol
        currPlayer=self.game.players[0]
        for tile in currPlayer.tiles:
            if tile.row<smallestRow:
                smallestRow=tile.row
                smallestCol=tile.column
            elif tile.row==smallestRow:
                smallestCol=min(tile.column,smallestCol)
        
        return smallestRow,smallestCol
    
    def orderedStrategy(self):

        print(self.game.players[0])

        if self.game.gameEnd():
            return self.game.players[0].name+" has won the game!"
        
        smallestHotel="Worldwide"
        smallestRow,smallestCol=self.minTile(15,15)

        for hotel in self.game.board.allHotels.keys():
            if self.game.board.allHotels[hotel]["placed"]==False:
                smallestHotel=min(smallestHotel,hotel)
        
        self.game.place(smallestRow,smallestCol,smallestHotel)

        shareCount=3
        for hotel in self.game.board.allHotels.keys():
            while shareCount>0:
                if not self.game.buy(hotel):
                    break
                else:
                    shareCount-=1
        self.game.done()

        #print(self.game.getStateObj())
        print(self.game.board.printB())
        return self.orderedStrategy()


        #print(smallestRow,smallestCol)
    


    def randomStrategy(self):
        pass

    def playGame(self):
        self.setupGame()
        if self.p1_strategy==1:
            self.orderedStrategy()
        else:
            self.randomStrategy()
        return 1

g=GamePlay()
print(g.playGame())
