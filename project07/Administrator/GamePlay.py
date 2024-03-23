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

    def orderedStrategy(self):

        print("Player playing: "+self.game.players[0].name)
        print("Current state of players:")
        print(self.game.players[0].getPlayerObj())
        print(self.game.players[1].getPlayerObj())

        currPlayer=self.game.players[0]
        sorted_tiles = sorted(currPlayer.tiles, key=lambda tile: (tile.row, tile.column))
        smallestHotel="Worldwide"
        smallestRow=sorted_tiles[0].row
        smallestCol=sorted_tiles[0].column

        for hotel in self.game.board.allHotels.keys():
            if self.game.board.allHotels[hotel]["placed"]==False:
                smallestHotel=min(smallestHotel,hotel)
        
        res=self.game.place(smallestRow,smallestCol,smallestHotel)

        maxtries=5
        while not res and maxtries>0:
            maxtries-=1
            sorted_tiles.append(sorted_tiles.pop(0))
            smallestRow=sorted_tiles[0].row
            smallestCol=sorted_tiles[0].column
            res=self.game.place(smallestRow,smallestCol,smallestHotel)

        if maxtries==0 and not res:
            return self.game.players[0].name+" has no possible moves. "+self.game.players[1].name+" wins the game!"
        
        if self.game.gameEnd():
            return self.game.players[0].name+" wins the game!"

        shareCount=3
        for hotel in self.game.board.allHotels.keys():
            while shareCount>0:
                res=self.game.buy(hotel)
                if not res:
                    break
                else:
                    shareCount-=1
        self.game.done()

        print(self.game.board.printB())

        print("Turn Over")
        print("=============================================================>")
        return self.orderedStrategy()


        #print(smallestRow,smallestCol)
    


    def randomStrategy(self):
        pass

    def playGame(self):
        self.setupGame()
        if self.p1_strategy==1:
            print(self.orderedStrategy())
        else:
            self.randomStrategy()

g=GamePlay()
g.playGame()
