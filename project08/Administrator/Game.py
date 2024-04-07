from Player import Player
from Board import Board
from Hotel import Hotel
from Share import Share
from Tiles import Tiles
from AutomatedPlayer import AutomatedPlayer
from shareDict import shareDict
import heapq
import random


class Game:

    def __init__(self,state=None,mode=None,players=None):
        self.mode=mode
        self.allTiles = []
        for i in range(1, 13):
            for j in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]:
                self.allTiles.append(Tiles(j, i))
        self.initializeState(state,players=players)

    def removeAvlTile(self,tile):
        for i in range(len(self.allTiles)):
            if self.allTiles[i] == tile:
                return self.allTiles.pop(i)
        return False

    def pickRandomTile(self):
        if len(self.allTiles)<2:
            return False
        num = random.randint(0, len(self.allTiles) - 1)
        tile = self.allTiles[num]
        return self.removeAvlTile(tile)


    def getStateObj(self):
        p = []
        for ply in self.players:
            p.append(ply.getPlayerObj())
        return {"board": self.board.getBoardObject(), "players": p}

    def setup(self,players,strategies=None):

        self.initializeState(None,players=players,strategies=strategies)
        if len(players) <= 6:
            for player in self.players:
                curPlayerTiles = []
                for i in range(6):
                    curPlayerTiles.append(self.pickRandomTile())
                player.tiles += curPlayerTiles
        else:
            return {"error": "More than 6 players"}

        return self.getStateObj()

    def getShareObj(self, shareState):
        return Share(shareState["share"], shareState["count"])

    def getTileObj(self, tileState):
        return Tiles(tileState.row, tileState.column)

    def getPlayerObj(self, playerState):
        shares = []
        for share in playerState["shares"]:
            shares.append(self.getShareObj(share))
        tiles = []
        for tile in playerState["tiles"]:
            tiles.append(Tiles(tile["row"],tile["column"]))

        return Player(playerState["player"], playerState["cash"], shares, tiles)
    
    def removeTilesAfterPlace(self):
        for tile in self.board.tiles:
            self.removeAvlTile(tile)

    def place(self, row, col, hotel=None):
        merge_copy = {}
        for hotelname in self.board.allHotels:
            merge_copy[hotelname] = self.board.allHotels[hotelname]["dataObj"].tiles

        if Tiles(row, col) in self.assignedTiles:
            return {"error": "Tile already on board"}

        players = self.players[0]

        flg = True
        for tile in players.tiles:
            if row == tile.row and col == tile.column:
                flg = False
                break
        if flg:
            return {"error": "Not a valid tile for this player"}
        
        res, hotellist = self.board.placeTile(Tiles(row, col), hotel)

        # If successful remove tile from player
        if res != "error":
            updatedtiles = []
            for tile in players.tiles:
                if row != tile.row or col != tile.column:
                    updatedtiles.append(self.getTileObj(tile))
            for player in self.players:
                if player.name == players.name:
                    player.tiles = updatedtiles
        else:
            print("Place request unsuccessful for "+str(Tiles(row,col).getTileObj()))
            return False

        self.removeTilesAfterPlace()

        if res == "founding" and self.numShares[hotel] != 0:
            for player in self.players:
                if player.name == players.name:
                    player.addShareForPlayer(hotel, 1)
                    self.numShares[hotel] -= 1
                    self.assignedShares[hotel][player.name] += 1

        if res == "merging":
            merge_res=self.hotel_merge_pay(hotellist,merge_copy)

        # self.board.printB()
        print("*****") 
        print("Tile placed at "+str(Tiles(row,col).getTileObj())) 
        print("Action: "+res)
        print("*****")
        return self.getStateObj()
    
    def payout(self,playername,price,hotel):
        for player in self.players:
                        if player.name == playername:
                            player.cash += price
                            self.assignedShares[hotel][playername] = 0
                            sharecnt=player.trackShareForPlayer(hotel)
                            self.numShares[hotel]+=sharecnt
                            player.removeShareForPlayer(hotel)

    
    def hotel_merge_pay(self,hotellist,merge_copy):
        stockholders = self.merger_payout(hotellist)
        if stockholders == "error":
                return self.getStateObj()

        for hotel in stockholders:
            price = shareDict[hotel][len(merge_copy[hotel])] if len(merge_copy[hotel])<=41 else shareDict[hotel][41]
            num_majority=len(stockholders[hotel][0])
            num_minority=len(stockholders[hotel][1])
            
            price_majority = price*15/num_majority if num_majority>1 else price*10
            price_minority = price*5/num_minority if num_minority>0 else 0
    
            for playername in stockholders[hotel][0]:
                self.payout(playername, round(price_majority), hotel)
                
            for playername in stockholders[hotel][1]:
                self.payout(playername, round(price_minority), hotel)
        return False


    def initializeShares(self):
        for key in self.assignedShares:
            for player in self.players:
                if player.name in self.assignedShares[key]:
                    continue
                else:
                    self.assignedShares[key][player.name] = player.trackShareForPlayer(
                        key
                    )
                    self.numShares[key] -= player.trackShareForPlayer(key)

    def initializeState(self, state, players=None,strategies=None):
        self.numShares = {
            "Worldwide": 25,
            "Sackson": 25,
            "Festival": 25,
            "Imperial": 25,
            "American": 25,
            "Continental": 25,
            "Tower": 25,
        }
        self.assignedShares = {
            "Worldwide": {},
            "Sackson": {},
            "Festival": {},
            "Imperial": {},
            "American": {},
            "Continental": {},
            "Tower": {},
        }
        self.players = []
        self.assignedTiles = []
        
        if state:
            
            self.board = Board(state["board"]["tiles"], state["board"]["hotels"])
            if len(state["players"]) > 6:
                raise Exception({"error": "Max number of allowed players is 6"})

            for player in state["player"]:
                self.players.append(self.getPlayerObj(player))

            for tile in state["board"]["tiles"]:
                tile = Tiles(tile["row"],tile["column"])
                self.assignedTiles.append(tile)
                self.removeAvlTile(tile)

            self.initializeShares()

            for key in self.numShares.keys():
                self.numShares[key]=0

            for share in player["share"]:
                self.numShares[share.name]+=share.count

        elif players and not self.mode:
            
            self.board = Board([], [])
            for player in players:
                    self.players.append(Player(player, 6000, [], []))
            self.initializeShares()

        elif players and self.mode=='automated':
            
            self.board = Board([], [])
            i=0
            for player in players:
                    if strategies[i] == 1:
                        playerStrategy = 1
                    elif strategies[i] == 2:
                        playerStrategy = 2
                    elif strategies[i] == 3:
                        playerStrategy = 3
                    elif strategies[i] == 4:
                        playerStrategy = 4
                    self.players.append(AutomatedPlayer(player, 6000, [], [], playerStrategy))
                    i+=1
            self.initializeShares()
        else:
            
            self.board = Board([], [])

    def merger_payout(self, hotellist):
        stockholders = {}
        for hotel in hotellist[1]:
            heap = []
            for key, val in self.assignedShares[hotel].items():
                if val != 0:
                    heapq.heappush(heap, (-1 * val, key))
            majority = []
            minority = []
            if heap:
                maxval, maxshare = heapq.heappop(heap)
            else:
                break
            maxval = -1 * maxval
            majority.append(maxshare)
            while heap:
                smaxval, smaxshare = heapq.heappop(heap)
                smaxval = -1 * smaxval
                if smaxval == maxval:
                    majority.append(smaxshare)
                else:
                    minority.append(smaxshare)

            stockholders[hotel] = [majority, minority]

        return stockholders if stockholders else "error"

    def buyShare(self, hotel, count, player):
        if shareDict[hotel.label][len(hotel.tiles)] == 0:
            return False
        if (
            self.numShares[hotel.label] > 0
            and shareDict[hotel.label][len(hotel.tiles)] * count <= player.cash
        ):
            player.addShareForPlayer(hotel.label, count)
            self.assignedShares[hotel.label][player.name] += count
            player.cash -= shareDict[hotel.label][len(hotel.tiles)] * count
            self.numShares[hotel.label]-=1
            return True
        return False

    def buy(self,hotelName):
        if self.buyShare(self.board.allHotels[hotelName]["dataObj"], 1, self.players[0])== False:
            #print("error: Not enough money to buy shares or hotel not established!")
            return False
        return self.getStateObj()

    def done(self):
        res=self.pickRandomTile()
        if not res:
            return False
        self.players[0].tiles.append(res)
        self.players.append(self.players.pop(0))
        return self.getStateObj()

    def gameEnd(self):
        safeHotels=0
        hotelsOnBoard=0

        for hotel in self.board.allHotels.keys():
            if self.board.allHotels[hotel]["placed"]:
                hotelsOnBoard += 1
                if len(self.board.allHotels[hotel]["dataObj"].tiles) >= 41:
                    return True
                elif len(self.board.allHotels[hotel]["dataObj"].tiles) >= 11:
                    safeHotels += 1

        if safeHotels == hotelsOnBoard and safeHotels!=0:
            return True
        
        return False

    def declare_winner(self):
        merge_copy = {}
        hotels=[]
        currCash={}
        for hotelname in self.board.allHotels:
            merge_copy[hotelname] = self.board.allHotels[hotelname]["dataObj"].tiles
            hotels.append(hotelname)
        hotellist=[[],hotels]
        res=self.hotel_merge_pay(hotellist,merge_copy)
        for player in self.players:
            currCash[player.name]=player.cash
        print("Final Payout Completed")
        winner=self.players[0].name
        for player in currCash:
            print(player+" has "+str(currCash[player]))
            if currCash[player]>currCash[winner]:
                winner=player
        return winner
                


#game = Game([])

#print(game.handleRequest({"request": "setup", "players": ["A", "B", "C"]}))
