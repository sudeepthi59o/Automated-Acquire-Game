from Game import Game
import random

class AutomatedGamePlay:
    def __init__(self,state=None,test_mode=None) -> None:
        self.game=Game(state)
        self.game.mode='automated'
        self.test_mode=test_mode
        self.players_without_vaild_moves=set()
        self.hotels=list(self.game.board.allHotels.keys())
        self.randomTries=10


    def setupGame(self):
        self.p1_strategy=1
        self.p2_strategy=2
        self.p3_strategy=3
        self.p4_strategy=4
        #Pick a strategy for the game: 1 - Ordered, 2 - Random, 3 - Alphabetical, 4- Anti Alphabetical 
        self.game.setup(players=["Player1","Player2","Player3","Player4"],strategies=[self.p1_strategy,self.p2_strategy,self.p3_strategy,self.p4_strategy])

    def no_valid_moves(self):
        print("Turn Over")
        print("=============================================================>")
        self.game.players.append(self.game.players.pop(0))
        return self.nextTurn()
    
    def nextTurn(self):
        if self.test_mode:
            return False
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
    

    def strategy(self,tile,order):
        if not self.test_mode:
            self.printCurrentStateOfPlayer()
        
        currPlayer=self.game.players[0]
        if tile == "des":
            sorted_tiles = sorted(currPlayer.tiles, key=lambda tile: (tile.row, tile.column),reverse=True)
        else:
            sorted_tiles = sorted(currPlayer.tiles, key=lambda tile: (tile.row, tile.column))
        smallestHotel="Worldwide"
        tile_row=sorted_tiles[0].row
        tile_column=sorted_tiles[0].column

        for hotel in self.game.board.allHotels.keys():
            if self.game.board.allHotels[hotel]["placed"]==False:
                smallestHotel=order(smallestHotel,hotel)
        
        res=self.game.place(tile_row,tile_column,smallestHotel)

        maxtries=5                              #5 tries to place a tile
        while not res and maxtries>0:
            maxtries-=1
            sorted_tiles.append(sorted_tiles.pop(0))
            tile_row=sorted_tiles[0].row
            tile_column=sorted_tiles[0].column
            res=self.game.place(tile_row,tile_column,smallestHotel)
        
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
        
        resdone=self.game.done()
        if not resdone:
            print("=============================================================>")
            print("Out of tiles")
            winner=self.game.declare_winner()
            return winner+ " wins the game!!"

        return self.nextTurn()

    def orderedStrategy(self):
        print("InOrderedStartegy")
        return self.strategy("asc",min)

    def alphabeticalStrategy(self):
        print("InAlphabeticalStrategy")
        return self.strategy("des",min)

    def anti_alphabeticalStrategy(self):
        print("In-AntiAlphabeticalStrategy")
        return self.strategy("asc",max)
    
    def getRandomTile(self,player):
        tile_num=random.randint(0,5)
        return player.tiles[tile_num]
    
    def getRandomHotel(self):
        hotel_num=random.randint(0,6)
        return self.hotels[hotel_num]
    
    def getRandomShares(self):
        share_num=random.randint(0,3)
        return share_num

    def randomStrategy(self):
        print("InRandomStrategy")
        if not self.test_mode:
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

        return self.nextTurn()

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
