from Player import Player
from Board import Board
from Hotel import Hotel
from Share import Share
from Tiles import Tiles
from shareDict import shareDict
import heapq
import json
import os
import random


class Game:

    def __init__(self, state=None, players=None):
        self.initializeState(state, players)
        self.allTiles = []
        for i in range(1, 13):
            for j in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]:
                self.allTiles.append(Tiles(j, i))

    def removeAvlTile(self, tile):
        for i in range(len(self.allTiles)):
            if self.allTiles[i] == tile:
                return self.allTiles.pop(i)
        return False

    def pickRandomTile(self):
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

    def setup(self, players):
        # self.board = Board([], [])
        # self.players = []
        # self.assignedTiles = []
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
        return Share(shareState["share"], shareState["count"])

    def getTileObj(self, tileState):
        return Tiles(tileState["row"], tileState["column"])

    def getPlayerObj(self, playerState):
        shares = []
        for share in playerState["shares"]:
            shares.append(self.getShareObj(share))
        tiles = []
        for tile in playerState["tiles"]:
            tiles.append(self.getTileObj(tile))

        return Player(playerState["player"], playerState["cash"], shares, tiles)

    def place(self, row, col, state, hotel=None):
        self.initializeState(state)
        # self.board = Board(state["board"]["tiles"], state["board"]["hotels"])
        # self.board.printB()
        merge_copy = {}
        for hotelname in self.board.allHotels:
            merge_copy[hotelname] = self.board.allHotels[hotelname]["dataObj"].tiles

        if Tiles(row, col) in self.assignedTiles:
            return {"error": "Tile already on board"}
        # self.players = []
        # for player in state["players"]:
        #     self.players.append(self.getPlayerObj(player))
        # self.initializeShares()
        players = state["players"][0]
        flg = True
        for tile in players["tiles"]:
            if row == tile["row"] and col == tile["column"]:
                flg = False
                break
        if flg:
            return {"error": "Not a valid tile for this player"}
        res, hotellist = self.board.placeTile(Tiles(row, col), hotel)

        # If successful remove tile from player
        if res != "error":
            updatedtiles = []
            for tile in players["tiles"]:
                if row != tile["row"] or col != tile["column"]:
                    updatedtiles.append(self.getTileObj(tile))
            for player in self.players:
                if player.name == players["player"]:
                    player.tiles = updatedtiles
        else:
            return {"error": "Place request unsuccessful"}

        if res == "founding" and self.numShares[hotel] != 0:
            for player in self.players:
                if player.name == players["player"]:
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

    def buy(self, shares, state):
        self.initializeState(state)
        # self.board = Board(state["board"]["tiles"], state["board"]["hotels"])
        # for player in state["players"]:
        #     self.players.append(self.getPlayerObj(player))
        # self.initializeShares()
        for hotelName in shares:
            if (
                self.buyShare(
                    self.board.allHotels[hotelName]["dataObj"], 1, self.players[0]
                )
                == False
            ):
                return {
                    "error": "Not enough money to buy shares or hotel not established!"
                }
        return self.getStateObj()

    def done(self, state):
        self.initializeState(state)
        # self.board = Board(state["board"]["tiles"], state["board"]["hotels"])
        # self.assignedTiles = []
        # for tile in state["board"]["tiles"]:
        #     tile = self.getTileObj(tile)
        #     self.assignedTiles.append(tile)
        # for player in state["players"]:
        #     self.players.append(self.getPlayerObj(player))
        # self.initializeShares()
        self.players[0].tiles.append(self.pickRandomTile())
        self.players.append(self.players.pop(0))
        return self.getStateObj()

    def handleRequest(self, request):
        try:
            if request["request"] == "setup":
                return self.setup(request["players"])
            elif request["request"] == "place":
                return self.place(
                    request["row"],
                    request["column"],
                    request["state"],
                    request["hotel"] if ("hotel" in request) else None,
                )
            elif request["request"] == "buy":
                return self.buy(request["shares"], request["state"])
            elif request["request"] == "done":
                return self.done(request["state"])

        except Exception as e:
            return {"error": "Invalid request", "message": e}


game = Game([])

# print(game.handleRequest({"request": "setup", "players": ["A", "B", "C"]}))
# print(game.handleRequest({
#     "request": "place",
#     "row": "C",
#     "column": "5",
#     "hotel": "Tower",
#     "state": {
#         "board": {
#             "tiles": [
#                 {
#                     "row": "B",
#                     "column": "3"
#                 },
#                 {
#                     "row": "B",
#                     "column": "2"
#                 },
#                 {
#                     "row": "C",
#                     "column": "2"
#                 },
#                 {
#                     "row": "C",
#                     "column": "6"
#                 }
#             ],
#             "hotels": [
#                 {
#                     "hotel": "Sackson",
#                     "tiles": [
#                         {
#                             "row": "B",
#                             "column": "3"
#                         },
#                         {
#                             "row": "B",
#                             "column": "2"
#                         },
#                         {
#                             "row": "C",
#                             "column": "2"
#                         }
#                     ]
#                 }
#             ]
#         },
#         "players": [
#             {
#                 "player": "A",
#                 "cash": 6000,
#                 "shares": [],
#                 "tiles": [
#                     {
#                         "row": "F",
#                         "column": "8"
#                     },
#                     {
#                         "row": "C",
#                         "column": "5"
#                     },
#                     {
#                         "row": "G",
#                         "column": "9"
#                     },
#                     {
#                         "row": "D",
#                         "column": "5"
#                     },
#                     {
#                         "row": "I",
#                         "column": "12"
#                     },
#                     {
#                         "row": "C",
#                         "column": "4"
#                     }
#                 ]
#             },
#             {
#                 "player": "B",
#                 "cash": 6000,
#                 "shares": [],
#                 "tiles": [
#                     {
#                         "row": "F",
#                         "column": "7"
#                     },
#                     {
#                         "row": "E",
#                         "column": "6"
#                     },
#                     {
#                         "row": "A",
#                         "column": "1"
#                     },
#                     {
#                         "row": "A",
#                         "column": "2"
#                     },
#                     {
#                         "row": "D",
#                         "column": "6"
#                     },
#                     {
#                         "row": "E",
#                         "column": "7"
#                     }
#                 ]
#             }
#         ]
#     }
# }))
