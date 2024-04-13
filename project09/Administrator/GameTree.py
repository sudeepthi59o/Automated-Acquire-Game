from Player import Player
from Board import Board
from Hotel import Hotel
from Share import Share
from Tiles import Tiles
from Game import Game
import random
import copy

class GameTreeAdmin:
    def __init__(self,game) -> None:
        self.game=game
        self.hotellist=list(game.board.allHotels.keys())
    
    def getRandomHotel(self):
        hotel_num=random.randint(0,6)
        return hotel_num
    
    def isGameDone(self):
        if self.game.gameEnd():
            return True
        return False
    
    def replace_tile(self):
        tiles=self.game.player[0].tiles
        tiles.pop(0)
        self.game.player[0].tiles=tiles
        res=self.game.done()
        self.cnt=0
        if not res:
            self.canContinueGame()

    def canContinueGame(self):
        if self.cnt==6:
            return True
        count=0
        for key,value in self.children.items():
            if not value:
                count+=1
        return True if count<6 else False

    def generate(self):
        self.children={}
        tiles=self.game.players[0].tiles
        for tile in tiles:
            print(tile.row,tile.column)
            self.children[(tile.row,tile.column)]=[]

        self.cnt=0
        for tile in self.children:
            for i in range(100):
                game_copy=copy.deepcopy(self.game)
                res=game_copy.place(tile[0],tile[1],self.hotellist[self.getRandomHotel()])
                if res=="error":
                    self.cnt+=1
                    break
                game_copy.buy(self.hotellist[self.getRandomHotel()])
                game_copy.buy(self.hotellist[self.getRandomHotel()])
                game_copy.buy(self.hotellist[self.getRandomHotel()])

                res_done=game_copy.done()
                if not res_done:
                    break
                self.children[(tile[0],tile[1])].append(game_copy)

        if self.cnt==6:
            self.replace_tile()
        return self.children



class GameTreePlayer:
    def __init__(self,children) -> None:
        self.tree=children
    
    def getRandomTile(self):
        tile_num=random.randint(0,5)
        return tile_num
    

    def pickChild(self,strategy,children):
        tiles=[Tiles(x,y) for x,y in self.tree.keys()]
        sorted_tiles = sorted(tiles, key=lambda tile: (tile.row, tile.column))
        if strategy=="ordered":
            tile=sorted_tiles[0]
        elif strategy=="random":
            tile=sorted_tiles[self.getRandomTile()]
        elif strategy=="largest-alpha":
            tile=sorted_tiles[-1]
        elif strategy=="smallest-anti":
            tile=sorted_tiles[0]
        
        pickedGame=self.tree[(tile.row,tile.column)][0]

        return pickedGame