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

    def __init__(self, state=None, players=None,mode=None):
        self.initializeState(state, players)
        self.allTiles = []
        self.mode=mode
        for i in range(1, 13):
            for j in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]:
                self.allTiles.append(Tiles(j, i))

    def removeAvlTile(self, tile):
        for i in range(len(self.allTiles)):
            if self.allTiles[i] == tile:
                return self.allTiles.pop(i)
        return False

    def pickRandomTile(self):
        if len(self.allTiles)<2:
            raise ValueError("No more tiles")
        num = random.randint(0, len(self.allTiles) - 1)
        tile = self.allTiles[num]
        return self.removeAvlTile(tile)

        # while len(self.assignedTiles) <= 12 * 9:
        #     num = random.randint(0, 107)
        #     row = int(num / 12)
        #     col = int(num / 9)
        #     if Tiles(row, col) not in self.assignedTiles:
        #         self.assignedTiles.append(Tiles(row, col))
        #         return Tiles(row, col)

    def getStateObj(self):
        p = []
        for ply in self.players:
            p.append(ply.getPlayerObj())
        return {"board": self.board.getBoardObject(), "players": p}

    def setup(self, players,strategies=1):
        # self.board = Board([], [])
        # self.players = []
        # self.assignedTiles = []
        if self.mode=='automated':
            for player in players:
                    self.players.append(AutomatedPlayer(player, 6000, [], [],'ordered' if strategies==1 else 'random'))
            self.initializeShares()
        else:
            self.initializeState(None, players)
        if len(players) <= 6:
            for player in self.players:
                curPlayerTiles = []
                for i in range(6):
                    curPlayerTiles.append(self.pickRandomTile())
                player.tiles += curPlayerTiles
            # playerObj = Player(player, 6000, [], curPlayerTiles)
            # self.players.append(playerObj)
        else:
            return {"error": "More than 6 players"}
        # print(self.players)
        # self.initializeShares()
        return self.getStateObj()

    def getShareObj(self, shareState):
        return Share(shareState.share, shareState.count)

    def getTileObj(self, tileState):
        return Tiles(tileState.row, tileState.column)

    def getPlayerObj(self, playerState):
        shares = []
        for share in playerState.shares:
            shares.append(self.getShareObj(share))
        tiles = []
        for tile in playerState.tiles:
            tiles.append(self.getTileObj(tile))

        return AutomatedPlayer(playerState.name, playerState.cash, shares, tiles,self.players[0].strategy) if self.mode=='automated' else Player(playerState.name, playerState.cash, shares, tiles)
    
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
            print("error Place request unsuccessful")
            return False

        self.removeTilesAfterPlace()

        if res == "founding" and self.numShares[hotel] != 0:
            for player in self.players:
                if player.name == players.name:
                    player.addShareForPlayer(hotel, 1)
                    self.numShares[hotel] -= 1
                    self.assignedShares[hotel][player.name] += 1

        if res == "merging":
            stockholders = self.merger_payout(hotellist)
            if stockholders == "error":
                return self.getStateObj()

            for hotel in stockholders:
                price = shareDict[hotel][len(merge_copy[hotel])]
                maj_flag = False
                for playername in stockholders[hotel][0]:
                    if len(stockholders[hotel][0]) == 1:
                        for player in self.players:
                            if player.name == playername:
                                player.cash += price * 10
                                self.assignedShares[hotel][playername] = 0
                                player.removeShareForPlayer(hotel)
                        break

                    if len(stockholders[hotel][0]) > 1:
                        for player in self.players:
                            if player.name == playername:
                                player.cash += round(
                                    (price * 15) / len(stockholders[hotel][0])
                                )
                                self.assignedShares[hotel][playername] = 0
                                player.removeShareForPlayer(hotel)
                                maj_flag = True

                for playername in stockholders[hotel][1]:
                    if len(stockholders[hotel][1]) == 1 and not maj_flag:
                        for player in self.players:
                            if player.name == playername:
                                player.cash += price * 5
                                self.assignedShares[hotel][playername] = 0
                                player.removeShareForPlayer(hotel)
                        break

                    if len(stockholders[hotel][1]) > 1 and not maj_flag:
                        for player in self.players:
                            if player.name == playername:
                                player.cash += round(
                                    (price * 5) / len(stockholders[hotel][1])
                                )
                                self.assignedShares[hotel][playername] = 0
                                player.removeShareForPlayer(hotel)

        # self.board.printB()
        print("*****") 
        print(Tiles(row,col).getTileObj())                     
        print(res)
        print("*****")
        return self.getStateObj()

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
        # print(self.assignedShares)

    def initializeState(self, state, players=None):
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

            for player in state["players"]:
                self.players.append(self.getPlayerObj(player))

            for tile in state["board"]["tiles"]:
                tile = self.getTileObj(tile)
                self.assignedTiles.append(tile)
                self.removeAvlTile(tile)

            self.initializeShares()
        elif players:
            self.board = Board([], [])
            for player in players:
                    self.players.append(Player(player, 6000, [], []))
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
                return "error"
            maxval = -1 * maxval
            majority.append(maxshare)
            while heap:
                smaxval, smaxshare = heapq.heappop(heap)
                smaxval = -1 * smaxval
                if smaxval == maxval:
                    majority.append(smaxshare)
                else:
                    minority.append(smaxshare)
                    break

            while heap:
                nextval, nextshare = heapq.heappop(heap)
                nextval = -1 * nextval
                if nextval == minority[0]:
                    minority.append(nextshare)
                else:
                    break
            stockholders[hotel] = [majority, minority]

        return stockholders

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
            return True
        return False

    def buy(self,hotelName):
        if self.buyShare(self.board.allHotels[hotelName]["dataObj"], 1, self.players[0])== False:
            #print("error: Not enough money to buy shares or hotel not established!")
            return False
        return self.getStateObj()

    def done(self):
        self.players[0].tiles.append(self.pickRandomTile())
        self.players.append(self.players.pop(0))
        return self.getStateObj()

    def gameEnd(self):
        safeHotels=0
        hotelsOnBoard=0

        for hotel in self.board.allHotels.keys():
            if self.board.allHotels[hotel]["placed"]:
                hotelsOnBoard += 1
                if len(self.board.allHotels[hotel]["dataObj"].tiles) == 41:
                    return True
                elif len(self.board.allHotels[hotel]["dataObj"].tiles) >= 11:
                    safeHotels += 1

        if safeHotels == hotelsOnBoard and safeHotels!=0:
            return True
        
        return False
                


#game = Game([])

#print(game.handleRequest({"request": "setup", "players": ["A", "B", "C"]}))
