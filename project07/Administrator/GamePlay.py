from Game import Game
from AutomatedPlayer import AutomatedPlayer

class GamePlay:
    def __init__(self) -> None:
        self.game=Game()
        self.game.mode='automated'
        self.players_without_vaild_moves=set()

    def setupGame(self):
        self.p1_strategy=1
        #int(input('Pick a strategy for the game: 1 - Ordered, 2 - Random ---->'))  #Add validation for input
        self.p2_strategy=self.p1_strategy      #Assigning same strategy to both players
        self.game.setup(["Player A","Player B"],self.p1_strategy)

    def no_valid_moves(self):
        print("Turn Over")
        print("=============================================================>")
        self.game.players.append(self.game.players.pop(0))
        return self.orderedStrategy()

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
        
        if maxtries==0 and not res and len(self.players_without_vaild_moves)<len(self.game.players):
            self.players_without_vaild_moves.add(self.game.players[0].name)
            return self.no_valid_moves()
         
        if len(self.players_without_vaild_moves)==len(self.game.players):
            print("=============================================================>")
            print("No more possible moves by the players")
            winner=self.game.declare_winner()
            return winner+ " wins the game!!"

        if self.game.gameEnd():
            print("=============================================================>")
            print("Game Ended!")
            winner=self.game.declare_winner()
            return winner+ " wins the game!!"

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

    
    def getRandomTile(self):
        pass
    def getRandomHotel(self):
        pass

    def randomStrategy(self):

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
        
        if maxtries==0 and not res and len(self.players_without_vaild_moves)<len(self.game.players):
            self.players_without_vaild_moves.add(self.game.players[0].name)
            return self.no_valid_moves()
         
        if len(self.players_without_vaild_moves)==len(self.game.players):
            print("=============================================================>")
            print("No more possible moves by the players")
            winner=self.game.declare_winner()
            return winner+ " wins the game!!"

        if self.game.gameEnd():
            print("=============================================================>")
            print("Game Ended!")
            winner=self.game.declare_winner()
            return winner+ " wins the game!!"

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

    def playGame(self):
        self.setupGame()
        if self.p1_strategy==1:
            print(self.orderedStrategy())
        else:
            print(self.randomStrategy())

g=GamePlay()
g.playGame()
