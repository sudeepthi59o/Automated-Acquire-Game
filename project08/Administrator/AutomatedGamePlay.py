from Game import Game
import random

class AutomatedGamePlay:
    def __init__(self) -> None:
        self.game=Game()
        self.game.mode='automated'
        self.players_without_vaild_moves=set()
        self.hotels=list(self.game.board.allHotels.keys())
        self.randomTries=10

    def get_input(self):
        value = int(input("Pick a strategy for the player, 1 -> Ordered, 2 -> Random ----> "))
        if value in [1,2]:
            return value
        else:
            self.get_input()

    def setupGame(self):
        print("Player1")
        self.p1_strategy = self.get_input()
        print("Player2")
        self.p2_strategy = self.get_input()
        # self.p1_strategy=1
        # self.p2_strategy=2
        #int(input('Pick a strategy for the game: 1 - Ordered, 2 - Random ---->'))  
        self.game.setup(players=["Player A","Player B"],strategies=[self.p1_strategy,self.p2_strategy])

    def no_valid_moves(self):
        print("Turn Over")
        print("=============================================================>")
        self.game.players.append(self.game.players.pop(0))
        return self.nextTurn()
    
    def nextTurn(self):
        if self.game.players[0].strategy==1:
            return self.orderedStrategy()
        else:
            return self.randomStrategy()
        
    def printCurrentStateOfPlayer(self):
        print("Player playing: "+self.game.players[0].name)
        print("Current state of players:")
        for i in range(len(self.game.players)):
            print(str(self.game.players[i]))

    def orderedStrategy(self):
        self.printCurrentStateOfPlayer()
        
        currPlayer=self.game.players[0]
        sorted_tiles = sorted(currPlayer.tiles, key=lambda tile: (tile.row, tile.column))
        smallestHotel="Worldwide"
        smallestRow=sorted_tiles[0].row
        smallestCol=sorted_tiles[0].column

        for hotel in self.game.board.allHotels.keys():
            if self.game.board.allHotels[hotel]["placed"]==False:
                smallestHotel=min(smallestHotel,hotel)
        
        res=self.game.place(smallestRow,smallestCol,smallestHotel)

        maxtries=5                              #5 tries to place a tile
        while not res and maxtries>0:
            maxtries-=1
            sorted_tiles.append(sorted_tiles.pop(0))
            smallestRow=sorted_tiles[0].row
            smallestCol=sorted_tiles[0].column
            res=self.game.place(smallestRow,smallestCol,smallestHotel)
        
        if maxtries==0 and not res and len(self.players_without_vaild_moves)<len(self.game.players):
            self.players_without_vaild_moves.add(self.game.players[0].name)
            return self.no_valid_moves()
         
        if len(self.players_without_vaild_moves)==len(self.game.players):     #If all players have no valid moves - terminate the game
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

        self.game.board.printB()

        print("Turn Over")
        print("=============================================================>")
        return self.nextTurn()

    
    def getRandomTile(self,player):
        tile_num=random.randint(0,5)
        return player.tiles[tile_num]
    
    def getRandomHotel(self):
        hotel_num=random.randint(0,6)
        return self.hotels[hotel_num]
    
    def getRandomShares(self):
        share_num=random.randint(0,2)
        return share_num

    def randomStrategy(self):
        self.printCurrentStateOfPlayer()

        currPlayer=self.game.players[0]
        picked_tile = self.getRandomTile(currPlayer)
        pickedRow=picked_tile.row
        pickedCol=picked_tile.column

        pickedHotel=self.getRandomHotel()
        
        res=self.game.place(pickedRow,pickedCol,pickedHotel)

        maxtries=5                  #5 tries to place a tile
        while not res and maxtries>0:
            maxtries-=1
            picked_tile = self.getRandomTile(currPlayer)
            pickedRow=picked_tile.row
            pickedCol=picked_tile.column
            res=self.game.place(pickedRow,pickedCol,self.getRandomHotel())
        
        if self.randomTries<=0:                     #Try 10 player turns place the tile, else terminate the game
            print("=============================================================>")
            print("No valid moves by the players in 10 turns")
            print("Ending the game")
            winner=self.game.declare_winner()
            return winner+ " wins the game!!"
        
        if maxtries==0 and not res:
            self.randomTries-=1 
            #self.players_without_vaild_moves.add(self.game.players[0].name)
            return self.no_valid_moves()

        if self.game.gameEnd():
            print("=============================================================>")
            print("Game Ended!")
            winner=self.game.declare_winner()
            return winner+ " wins the game!!"

        share_tries=5                   # Try to buy a random number of shares from a random hotel five times
        shareCount=self.getRandomShares()
        buy_from_hotel=self.getRandomHotel()
        while shareCount>0 and share_tries>0:
            res=self.game.buy(buy_from_hotel)
            share_tries-=1
            if not res:
                buy_from_hotel=self.getRandomHotel()
            else:
                shareCount-=1
        
        resdone=self.game.done()
        if not resdone:
            print("=============================================================>")
            print("Out of tiles")
            winner=self.game.declare_winner()
            return winner+ " wins the game!!"


        self.game.board.printB()

        print("Turn Over")
        print("=============================================================>")
        return self.nextTurn()

    def playGame(self):
        self.setupGame()
        if self.p1_strategy==1:
            print(self.orderedStrategy())
        else:
            print(self.randomStrategy())

g=AutomatedGamePlay()
g.playGame()
