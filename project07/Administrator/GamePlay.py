from Game import Game
from AutomatedPlayer import AutomatedPlayer
import random

class GamePlay:
    def __init__(self) -> None:
        self.game=Game()
        self.game.mode='automated'
        self.players_without_vaild_moves=set()
        self.hotels=list(self.game.board.allHotels.keys())
        self.randomTries=20

    def setupGame(self):
        self.p1_strategy=2
        #int(input('Pick a strategy for the game: 1 - Ordered, 2 - Random ---->'))  #Add validation for input
        self.p2_strategy=self.p1_strategy      #Assigning same strategy to both players
        self.game.setup(["Player A","Player B"],self.p1_strategy)

    def no_valid_moves_ordered(self):
        print("Turn Over")
        print("=============================================================>")
        self.game.players.append(self.game.players.pop(0))
        return self.orderedStrategy()
    
    def no_valid_moves_random(self):
        print("Turn Over")
        print("=============================================================>")
        self.game.players.append(self.game.players.pop(0))
        return self.randomStrategy()

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
            return self.no_valid_moves_ordered()
         
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

        print("Player playing: "+self.game.players[0].name)
        print("Current state of players:")
        print(self.game.players[0].getPlayerObj())
        print(self.game.players[1].getPlayerObj())

        currPlayer=self.game.players[0]
        picked_tile = self.getRandomTile(currPlayer)
        pickedRow=picked_tile.row
        pickedCol=picked_tile.column

        pickedHotel=self.getRandomHotel()
        
        res=self.game.place(pickedRow,pickedCol,pickedHotel)

        maxtries=5
        while not res and maxtries>0:
            maxtries-=1
            picked_tile = self.getRandomTile(currPlayer)
            pickedRow=picked_tile.row
            pickedCol=picked_tile.column
            res=self.game.place(pickedRow,pickedCol,self.getRandomHotel())
        
        if self.randomTries<=0:
            print("=============================================================>")
            print("No valid moves by the players in 20 turns")
            print("Ending the game")
            winner=self.game.declare_winner()
            return winner+ " wins the game!!"
        
        if maxtries==0 and not res:
            self.players_without_vaild_moves.add(self.game.players[0].name)
            self.randomTries-=1     #Try 20 player turns place the tile, else terminate the game
            return self.no_valid_moves_random()

        if self.game.gameEnd():
            print("=============================================================>")
            print("Game Ended!")
            winner=self.game.declare_winner()
            return winner+ " wins the game!!"

        share_tries=5
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


        print(self.game.board.printB())

        print("Turn Over")
        print("=============================================================>")
        return self.randomStrategy()

    def playGame(self):
        self.setupGame()
        if self.p1_strategy==1:
            print(self.orderedStrategy())
        else:
            print(self.randomStrategy())

g=GamePlay()
g.playGame()
