class Tiles:
    def __init__(self, row, column):
        self.row = None
        if type(row) == type(" "):
            self.row = int(ord(row) - ord("A"))
            self.column = int(column) - 1
        else:
            self.row = row
            self.column = int(column)

        if self.row > 8 or self.column > 11:
            raise Exception("Invalid tile")

    def __str__(self):
        return str([chr(ord("A") + self.row), str(self.column + 1)])

    def __eq__(self, obj1):
        return self.row == obj1.row and self.column == obj1.column

    def getTileObj(self):
        return {"row": chr(ord("A") + self.row), "column": str(self.column + 1)}
