from Share import Share
from Tiles import Tiles


class AutomatedPlayer:
    def __init__(self, name, cash, shares: list[Share], tiles: list[Tiles],strategy) -> None:
        
        if not len(name) < 20 or not name.isascii():
            raise Exception("invalid player name")
        
        self.name = name
        self.cash = cash
        self.shares = shares
        self.tiles = tiles
        self.strategy=strategy

    def __str__(self):
        ans = []
        for tile in self.tiles:
            ans.append(str(tile))
        return (
            "Name: " + self.name + " Cash: " + str(self.cash) + " Tiles: " + " ".join(ans)
        )

    def getPlayerObj(self):
        s = []
        for share in self.shares:
            s.append(share.getShareObj())
        t = []
        for tile in self.tiles:
            t.append(tile.getTileObj())
        return {"player": self.name, "cash": self.cash, "shares": s, "tiles": t}

    def addShareForPlayer(self, name, count):
        for share1 in self.shares:
            if share1.name == name:
                share1.count += count
                return True
        self.shares.append(Share(name, count))
        return True

    def removeShareForPlayer(self,name):
        newShares=[]
        for share in self.shares:
            if share.name==name:
                continue
            else:
                newShares.append(share)
        self.shares=newShares
        return True
    
    def trackShareForPlayer(self,name):
        for share1 in self.shares:
            if share1.name == name:
                return share1.count
        return 0