class Share:
    def __init__(self, name: str, count: int):
        self.validNames = [
            "American",
            "Continental",
            "Festival",
            "Imperial",
            "Sackson",
            "Tower",
            "Worldwide",
        ]
        if name not in self.validNames:
            raise Exception("Invalid share name")

        if count > 25:
            raise Exception("Invalid share count")

        self.name = name
        self.count = count

    def getShareObj(self):
        return {"label": self.name, "count": self.count}
