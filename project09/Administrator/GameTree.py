from Player import Player
from Board import Board
from Hotel import Hotel
from Share import Share
from Tiles import Tiles
from Game import Game
import random
import copy
from itertools import permutations

class GameTreeAdmin:
    def __init__(self,game) -> None:
        self.game=game
    
    def getHotel(self):
        for key in self.game.board.allHotels:
            if not self.game.board.allHotels[key]["placed"]:
                return key
        return None
    
    def isGameDone(self):
        if self.game.gameEnd():
            return True
        if len(self.game.allTiles)<2:
            return True
        return False
    
    def replace_tile(self):
        tiles=self.game.player[0].tiles
        x=tiles.pop(0)
        self.game.player[0].tiles=tiles
        self.game.allTiles.append(x)
    
    def remove_duplicates(self,shares):
        not_duplicates=set()
        for perm in shares:
            not_duplicates.add(perm)
        
        return list(not_duplicates)
    
    def generate(self):
        self.children={}
        tiles=self.game.players[0].tiles
        for tile in tiles:
            self.children[(tile.row,tile.column)]={"share_list":[],"replacement_list":[],"hotel":None}

        error_cnt=0
        for tile in self.children:
                game_copy=copy.deepcopy(self.game)
                hotel=self.getHotel()
                res=game_copy.place(tile[0],tile[1],hotel)
                if res=="error":
                    error_cnt+=1
                    break
                available_shares=[]
                for key,value in game_copy.numShares.items():
                    for i in range(value):
                        available_shares.append(key)
                can_buy_shares=permutations(available_shares,3)
                self.children[tile]["share_list"].append(sorted(self.remove_duplicates(list(can_buy_shares)))[0])
                self.children[tile]["replacement_list"].append(sorted(game_copy.allTiles, key=lambda tile: (tile.row, tile.column))[0])
                self.children[tile]["hotel"]=hotel

        if error_cnt==6:
            self.replace_tile()

        return self.children


class GameTreePlayer:
    def __init__(self,children) -> None:
        self.tree=children
    
    def getRandomTile(self):
        tile_num=random.randint(0,5)
        return tile_num
    
    def getRandomNum(self,range):
        num=random.randint(0,range)
        return num
        
    def pickChild(self,strategy,children):
        tiles=[Tiles(x,y) for x,y in self.tree.keys()]
        sorted_tiles = sorted(tiles, key=lambda tile: (tile.row, tile.column))
        if strategy=="ordered":
            tile=sorted_tiles[0]
            to_buy=children[(tile.row,tile.column)]["share_list"][0]
            replace_tile=children[(tile.row,tile.column)]["replacement_list"][0]
            hotel=children[(tile.row,tile.column)]["hotel"]
        elif strategy=="random":
            tile=sorted_tiles[self.getRandomTile()]
            to_buy=children[(tile.row,tile.column)]["share_list"][self.getRandomNum(len(children[(tile.row,tile.column)]["share_list"])-1)]
            replace_tile=children[(tile.row,tile.column)]["replacement_list"][self.getRandomNum(len(children[(tile.row,tile.column)]["replacement_list"])-1)]
            hotel=children[(tile.row,tile.column)]["hotel"]
        elif strategy=="largest-alpha":
            tile=sorted_tiles[-1]
            to_buy=children[(tile.row,tile.column)]["share_list"][0]
            replace_tile=children[(tile.row,tile.column)]["replacement_list"][0]
            hotel=children[(tile.row,tile.column)]["hotel"]
        elif strategy=="smallest-anti":
            tile=sorted_tiles[0]
            to_buy=children[(tile.row,tile.column)]["share_list"][-1]
            replace_tile=children[(tile.row,tile.column)]["replacement_list"][0]
            hotel=children[(tile.row,tile.column)]["hotel"]
        
        return tile,to_buy,replace_tile,hotel