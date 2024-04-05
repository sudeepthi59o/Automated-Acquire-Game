from Hotel import Hotel
from Tiles import Tiles
from tabulate import tabulate


class Board:
    def __init__(self, tiles, hotels):
        ###############################################################
        # Initialization
        self.tiles = []
        self.board = [["" for _ in range(12)] for _ in range(9)]
        self.allHotels = {
            "American": {"dataObj": Hotel("American", []), "placed": False},
            "Continental": {"dataObj": Hotel("Continental", []), "placed": False},
            "Festival": {"dataObj": Hotel("Festival", []), "placed": False},
            "Imperial": {"dataObj": Hotel("Imperial", []), "placed": False},
            "Sackson": {"dataObj": Hotel("Sackson", []), "placed": False},
            "Tower": {"dataObj": Hotel("Tower", []), "placed": False},
            "Worldwide": {"dataObj": Hotel("Worldwide", []), "placed": False},
        }

        ###############################################################

        # Iterate over tiles and place them
        for tile in tiles:
            tile = Tiles(tile["row"], tile["column"])
            self.tiles.append(tile)
            self.board[tile.row][tile.column] = "O"

        for htl in hotels:
            t = []
            for tile in htl["tiles"]:
                tile = Tiles(tile["row"], tile["column"])
                self.board[tile.row][tile.column] = htl["hotel"]
                t.append(tile)
            self.addTilesToHotel(htl["hotel"], t)
            self.allHotels[htl["hotel"]]["placed"] = True

    def __str__(self):
        return tabulate(self.board, tablefmt="grid")

    def getAvailableHotelCount(self):
        count = 0
        for hotelName in self.allHotels:
            if self.allHotels[hotelName]["placed"] == False:
                count += 1
        return count

    def isHotel(self, hotelName):
        return hotelName in self.allHotels.keys()

    def addTilesToHotel(self, hotel, tiles: list[Tiles]):
        self.allHotels[hotel]["dataObj"].tiles += tiles

    def printB(self)->None:
         # Creating indexes for rows and columns
        rows = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        columns = [str(i) for i in range(1, 13)]

        # Creating a new board with row and column indexes
        indexed_board = [[None] + columns]  # Adding an empty cell for the top-left corner
        for i, row in enumerate(self.board):
            indexed_row = [rows[i]] + row
            indexed_board.append(indexed_row)

        # Printing the indexed board
        print(tabulate(indexed_board, tablefmt="grid"))

    def checkRowColCondition(self, row, col):
        if row < 0 or row > 8 or col < 0 or col > 11:
            return False
        return True

    def adjacentHelper(self, row, col):
        if not self.checkRowColCondition(row, col):
            return False
        returnDict = {
            "L": {"symbol": "0", "row": row, "column": col - 1},
            "R": {"symbol": "0", "row": row, "column": col + 1},
            "U": {"symbol": "0", "row": row - 1, "column": col},
            "D": {"symbol": "0", "row": row + 1, "column": col},
            "meta": {"hotel": 0, "empty": 0, "occupied": 0},
        }
        # Up
        if self.checkRowColCondition(row - 1, col):
            returnDict["U"]["symbol"] = self.board[row - 1][col]

        # down
        if self.checkRowColCondition(row + 1, col):
            returnDict["D"]["symbol"] = self.board[row + 1][col]
        # left
        if self.checkRowColCondition(row, col - 1):
            returnDict["L"]["symbol"] = self.board[row][col - 1]
        # right
        if self.checkRowColCondition(row, col + 1):
            returnDict["R"]["symbol"] = self.board[row][col + 1]

        currHotel=None
        for key in returnDict.keys():
            if key == "meta":
                continue
            if returnDict[key]["symbol"] == "O":
                returnDict["meta"]["occupied"] += 1
            elif returnDict[key]["symbol"] == "":
                returnDict["meta"]["empty"] += 1
            elif returnDict[key]["symbol"] == "0":
                continue
            else:
                if currHotel!=returnDict[key]["symbol"]:
                    currHotel=returnDict[key]["symbol"]
                    returnDict["meta"]["hotel"] += 1
        return returnDict

    def singleTon(self, row, col, adjacentDict):
        n = 4
        if row == 0 or row == 8:
            n -= 1
        if col == 0 or col == 11:
            n -= 1

        if adjacentDict["meta"]["empty"] == n or (self.getAvailableHotelCount() == 0 and adjacentDict["meta"]["hotel"]==0):
            return True

        return False

    def founding(self, row, col, adjacentDict):
        n = 4
        if row == 0 or row == 8:
            n -= 1
        if col == 0 or col == 11:
            n -= 1
        if (
            adjacentDict["meta"]["occupied"] + adjacentDict["meta"]["empty"] == n
            and self.getAvailableHotelCount() > 0
        ):
            return True
        return False

    def growing(self, row, col, adjacentDict):
        if adjacentDict["meta"]["hotel"] == 1:
            return True
        return False

    def merging(self, row, col, adjacentDict):
        if adjacentDict["meta"]["hotel"] >= 2:
            return True
        return False

    def updateBoard(self, tile: Tiles, symbol, addTiles=True):
        if addTiles:
            self.tiles.append(tile)

        self.board[tile.row][tile.column] = symbol

    def aquireHotels(self, hotelList, curTile: Tiles):
        maxHotel = self.allHotels[hotelList[0]]["dataObj"]
        for hotel in hotelList:
            if self.allHotels[hotel]["placed"] and len(maxHotel.tiles) < len(
                self.allHotels[hotel]["dataObj"].tiles
            ):
                maxHotel = self.allHotels[hotel]["dataObj"]
        for hotel in hotelList:
            if hotel != maxHotel.label:
                # Changing the symbols on the board
                for tile in self.allHotels[hotel]["dataObj"].tiles:
                    self.updateBoard(tile, maxHotel.label, False)

                # Add the tiles to maxHotel
                self.addTilesToHotel(
                    maxHotel.label, self.allHotels[hotel]["dataObj"].tiles
                )

                # Remove the tiles from currentHotel
                self.allHotels[hotel]["dataObj"].tiles = []

                # Make it unplaced
                self.allHotels[hotel]["placed"] = False
        self.updateBoard(curTile, maxHotel.label)
        self.addTilesToHotel(maxHotel.label, [curTile])
        return [maxHotel.label]
    
    # def checkGrowing(self,direction,row,col):
    #     if direction=='L':
    #         adjacentDict=self.adjacentHelper(row,col-1)
    #         if self.growing(row,col-1,adjacentDict):
    #             self.placeTile(Tiles(row,col-1))
    #     if direction=='R':
    #         adjacentDict=self.adjacentHelper(row,col+1)
    #         if self.growing(row,col+1,adjacentDict):
    #             self.placeTile(Tiles(row,col+1))
    #     if direction=='U':
    #         adjacentDict=self.adjacentHelper(row-1,col)
    #         if self.growing(row,col-1,adjacentDict):
    #             self.placeTile(Tiles(row-1,col))
    #     if direction=='D':
    #         adjacentDict=self.adjacentHelper(row+1,col)
    #         if self.growing(row,col-1,adjacentDict):
    #             self.placeTile(Tiles(row+1,col))
        

    def placeTile(self, tile: Tiles, hotel=None):
        row = tile.row
        col = tile.column
        adjacentDict = self.adjacentHelper(row, col)
        if self.singleTon(row, col, adjacentDict):
            self.updateBoard(tile, "O")
            return "singleton",None
        
        elif self.founding(row, col, adjacentDict):
            if hotel==None:
                return "error",None
            elif self.allHotels[hotel]["placed"] == True:
                for hotelname in self.allHotels:
                    if self.allHotels[hotelname]["placed"]==False:
                        hotel=hotelname

            self.allHotels[hotel]["placed"] = True
            self.updateBoard(tile, hotel)
            self.addTilesToHotel(hotel, [tile])
            for key in adjacentDict:
                if key != "meta" and adjacentDict[key]["symbol"] == "O":
                    self.updateBoard(
                        Tiles(adjacentDict[key]["row"], adjacentDict[key]["column"]),
                        hotel,
                    )
                    self.addTilesToHotel(
                        hotel,
                        [Tiles(adjacentDict[key]["row"], adjacentDict[key]["column"])],
                    )
            return "founding",None
        
        elif self.growing(row, col, adjacentDict):
            hotelName = ""
            for key in adjacentDict:
                if key != "meta" and self.isHotel(adjacentDict[key]["symbol"]):
                    hotelName = adjacentDict[key]["symbol"]
                    break

            self.updateBoard(tile, hotelName)
            self.addTilesToHotel(hotelName, [tile])

            for key in adjacentDict:
                if key != "meta" and adjacentDict[key]["symbol"] == "O":
                    # self.checkGrowing(key,row,col)
                    self.updateBoard(
                        Tiles(adjacentDict[key]["row"], adjacentDict[key]["column"]),
                        hotelName,
                    )
                    self.addTilesToHotel(
                        hotelName,
                        [Tiles(adjacentDict[key]["row"], adjacentDict[key]["column"])],
                    )
            return "growing",None
        
        elif self.merging(row, col, adjacentDict):
            adjacentHotels = []
            for key in adjacentDict:
                if key != "meta" and self.isHotel(adjacentDict[key]["symbol"]):
                    adjacentHotels.append(adjacentDict[key]["symbol"])
            for hotel in adjacentHotels:
                if len(self.allHotels[hotel]["dataObj"].tiles) >=11:
                    return "error",None
            res=self.aquireHotels(adjacentHotels, tile)
            
            acquired_hotels=[]
            for hotel in adjacentHotels:
                if hotel!=res[0]:
                    acquired_hotels.append(hotel)
            return "merging",[res,acquired_hotels]
        else:
            return "error",None

    def getBoardObject(self):
        tiles = []
        for tile in self.tiles:
            tiles.append(tile.getTileObj())

        hotels = []
        for key in self.allHotels.keys():
            if self.allHotels[key]["placed"] == True:
                hotels.append(self.allHotels[key]["dataObj"].getHotelObj())

        return {"tiles": tiles, "hotels": hotels}
