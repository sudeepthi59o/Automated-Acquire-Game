from Tiles import Tiles


class Hotel:
    def __init__(self, label, tiles: list[Tiles]):
        self.validNames = [
            "American",
            "Continental",
            "Festival",
            "Imperial",
            "Sackson",
            "Tower",
            "Worldwide",
        ]
        if label not in self.validNames:
            raise Exception("invalid hotel name")
        
        self.label = label
        self.tiles = tiles

    def __eq__(self, other):
        if type(other) == type(" ") and other == self.label:
            return True
        return self.label == other.label

    def __str__(self):
        return self.label

    def __gt__(self, other):
        if other == None:
            return True
        return len(other.tiles) < len(self.tiles)

    def getHotelObj(self):
        tiles = []
        for tile in self.tiles:
            tiles.append(tile.getTileObj())
        return {"hotel": self.label, "tiles": tiles}

