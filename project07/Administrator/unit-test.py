import pytest
from Board import Board
from Tiles import Tiles
from Hotel import Hotel
from Share import Share
from Player import Player
from Game import Game


@pytest.fixture
def sample_board():
    tiles = [
        {"row": "B", "column": "3"},
        {"row": "B", "column": "2"},
        {"row": "C", "column": "2"},
        {"row": "C", "column": "6"},
        {"row": "A", "column": "4"},
        {"row": "A", "column": "5"},
        {"row": "C", "column": "4"},
        {"row": "D", "column": "4"},
        {"row": "E", "column": "4"},
        {"row": "F", "column": "4"}
    ]
    hotels = [
        {
            "hotel": "Sackson",
            "tiles": [
                {"row": "B", "column": "3"},
                {"row": "B", "column": "2"},
                {"row": "C", "column": "2"}
            ]
        },
        {
            "hotel": "American",
            "tiles": [
                {"row": "A", "column": "4"},
                {"row": "A", "column": "5"}
            ]
        },
        {
            "hotel": "Tower",
            "tiles": [
                {"row": "C", "column": "4"},
                {"row": "D", "column": "4"},
                {"row": "E", "column": "4"},
                {"row": "F", "column": "4"}
            ]
        }
    ]
    return Board(tiles, hotels)


def test_getAvailableHotelCount(sample_board):
    assert sample_board.getAvailableHotelCount() == 4


def test_isHotel(sample_board):
    assert sample_board.isHotel("Sackson") == True
    assert sample_board.isHotel("Hilton") == False


def test_addTilesToHotel(sample_board):
    sample_board.addTilesToHotel("Sackson", [Tiles("C", 1)])
    assert len(sample_board.allHotels["Sackson"]["dataObj"].tiles) == 4


def test_checkRowColCondition(sample_board):
    assert sample_board.checkRowColCondition(0, 0) == True
    assert sample_board.checkRowColCondition(-1, 0) == False


def test_updateBoard(sample_board):
    sample_board.updateBoard(Tiles("D", 2), "O")
    assert sample_board.board[3][1] == "O"


def test_getBoardObject(sample_board):
    result = sample_board.getBoardObject()
    assert len(result["tiles"]) == 10
    assert len(result["hotels"]) == 3


def test_adjacentHelper(sample_board):
    result = sample_board.adjacentHelper(1, 2)
    assert result["L"]["symbol"] == 'Sackson'
    assert result["meta"]["empty"] == 3


def test_singleTon(sample_board):
    result = sample_board.singleTon(2, 5, sample_board.adjacentHelper(2, 5))
    result1 = sample_board.singleTon(2, 3, sample_board.adjacentHelper(2, 3))

    assert result == True
    assert result1 == False


def test_founding(sample_board):
    result = sample_board.founding(2, 7, sample_board.adjacentHelper(2, 7))
    result1 = sample_board.founding(2, 3, sample_board.adjacentHelper(2, 3))

    assert result == True
    assert result1 == False


def test_growing(sample_board):
    result = sample_board.growing(1, 3, sample_board.adjacentHelper(1, 3))
    result1 = sample_board.growing(5, 7, sample_board.adjacentHelper(5, 7))

    assert result == False
    assert result1 == False


def test_merging(sample_board):
    result = sample_board.merging(1, 3, sample_board.adjacentHelper(1, 3))
    result1 = sample_board.merging(5, 7, sample_board.adjacentHelper(5, 7))

    assert result == True
    assert result1 == False


def test_placeTile(sample_board):
    result = sample_board.placeTile(Tiles(5, 7), "Festival")
    result1 = sample_board.placeTile(Tiles(2, 6), "Festival")
    result2 = sample_board.placeTile(Tiles(2, 7), "Festival")
    result3 = sample_board.placeTile(Tiles(1, 3), "Festival")

    assert result[0] == 'singleton'
    assert result1[0] == 'founding'
    assert result2[0] == 'growing'
    assert result3[0] == 'merging'


def test_aquireHotels(sample_board):
    result = sample_board.aquireHotels(
        ["American", "Tower", "Sackson"], Tiles(1, 3))

    assert result == ["Tower"]

     # bug - check for 11 hotels - FIXED

# --------------------------Game.py-----------------------


@pytest.fixture
def sample_state():
    return {
        "board": {
            "tiles": [
                {"row": "B", "column": "3"},
                {"row": "B", "column": "2"},
                {"row": "C", "column": "2"},
                {"row": "C", "column": "6"},
                {"row": "A", "column": "4"},
                {"row": "A", "column": "5"},
                {"row": "C", "column": "4"},
                {"row": "D", "column": "4"},
                {"row": "E", "column": "4"},
                {"row": "F", "column": "4"}
            ],
            "hotels": [
                {
                    "hotel": "Sackson",
                    "tiles": [
                        {"row": "B", "column": "3"},
                        {"row": "B", "column": "2"},
                        {"row": "C", "column": "2"}
                    ]
                },
                {
                    "hotel": "American",
                    "tiles": [
                        {"row": "A", "column": "4"},
                        {"row": "A", "column": "5"}
                    ]
                },
                {
                    "hotel": "Tower",
                    "tiles": [
                        {"row": "C", "column": "4"},
                        {"row": "D", "column": "4"},
                        {"row": "E", "column": "4"},
                        {"row": "F", "column": "4"}
                    ]
                }
            ]
        },
        "players": [
            {
                "player": "A",
                "cash": 6000,
                "shares": [{"share": "American", "count": 2}, {"share": "Tower", "count": 3}, {"share": "Sackson", "count": 1}],
                "tiles": [
                    {"row": "B", "column": "4"},
                    {"row": "I", "column": "11"},
                    {"row": "G", "column": "9"},
                    {"row": "D", "column": "5"},
                    {"row": "I", "column": "12"},
                    {"row": "C", "column": "4"}
                ]
            },
            {
                "player": "B",
                "cash": 6000,
                "shares": [{"share": "American", "count": 1}, {"share": "Tower", "count": 2}, {"share": "Sackson", "count": 3}],
                "tiles": [
                    {"row": "F", "column": "7"},
                    {"row": "E", "column": "6"},
                    {"row": "A", "column": "1"},
                    {"row": "A", "column": "2"},
                    {"row": "D", "column": "6"},
                    {"row": "E", "column": "7"}
                ]
            }
        ]
    }


@pytest.fixture
def sample_game():
    return Game(None, ["Madhur", "Jenil", "Sudeepthi"])


def test_gameInit():
    with pytest.raises(Exception) as exc_info:
        game = Game(None, ["Madhur", "Jenil", "Sudeepthi",
                    "fsadfasfsasdsfsdfsfsfsss"])
    assert str(exc_info.value) == "invalid player name"

def test_pickRandomTile(sample_game):
    result = sample_game.pickRandomTile()
    #bug - initialize self.assignedTiles - Can't do this

    assert result.row <=8
    assert result.column <=11


def test_setup(sample_game):
    result = sample_game.setup(
        ["Madhur", "Jenil", "Sudeepthi", "A", "B", "C", "D"])
    result1 = sample_game.setup(["Madhur", "Jenil", "Sudeepthi", "A"])

    assert result == {'error': 'More than 6 players'}
    # can't test whole object since tiles are allotted randomnly
    assert len(result1['players'][0]['tiles']) == 6
    assert len(result1['players'][1]['tiles']) == 6
    assert len(result1['players'][2]['tiles']) == 6


def test_place(sample_game, sample_state):
    result = sample_game.place(2, 3, sample_state)

    assert result == {'error': 'Tile already on board'}


def test_merger_payout():
    # Need a way to use the state and initialize Game
    pass


def test_buy(sample_game, sample_state):
    result = sample_game.buy(["Festival"], sample_state)
    result1 = sample_game.buy(["Sackson", "Sackson"], sample_state)
    print(result1)
    assert result == {
        'error': 'Not enough money to buy shares or hotel not established!'}
    assert result1 == {'board': {'tiles': [{'row': 'B', 'column': '3'}, {'row': 'B', 'column': '2'}, {'row': 'C', 'column': '2'}, {'row': 'C', 'column': '6'}, {'row': 'A', 'column': '4'}, {'row': 'A', 'column': '5'}, {'row': 'C', 'column': '4'}, {'row': 'D', 'column': '4'}, {'row': 'E', 'column': '4'}, {'row': 'F', 'column': '4'}], 'hotels': [{'hotel': 'American', 'tiles': [{'row': 'A', 'column': '4'}, {'row': 'A', 'column': '5'}]}, {'hotel': 'Sackson', 'tiles': [{'row': 'B', 'column': '3'}, {'row': 'B', 'column': '2'}, {'row': 'C', 'column': '2'}]}, {'hotel': 'Tower', 'tiles': [{'row': 'C', 'column': '4'}, {'row': 'D', 'column': '4'}, {'row': 'E', 'column': '4'}, {'row': 'F', 'column': '4'}]}]}, 'players': [
        {'player': 'A', 'cash': 5400, 'shares': [{'label': 'American', 'count': 2}, {'label': 'Tower', 'count': 3}, {'label': 'Sackson', 'count': 3}], 'tiles': [{'row': 'B', 'column': '4'}, {'row': 'I', 'column': '11'}, {'row': 'G', 'column': '9'}, {'row': 'D', 'column': '5'}, {'row': 'I', 'column': '12'}, {'row': 'C', 'column': '4'}]}, {'player': 'B', 'cash': 6000, 'shares': [{'label': 'American', 'count': 1}, {'label': 'Tower', 'count': 2}, {'label': 'Sackson', 'count': 3}], 'tiles': [{'row': 'F', 'column': '7'}, {'row': 'E', 'column': '6'}, {'row': 'A', 'column': '1'}, {'row': 'A', 'column': '2'}, {'row': 'D', 'column': '6'}, {'row': 'E', 'column': '7'}]}]}


def test_done(sample_game, sample_state):
    # bug - self.players should be overridden with the passed board state
    # need one function to initialize Game using the passed state
    result = Game(None, ["AAAA", "BBBB"]).done(sample_state)
    print(result)
    assert len(result["players"][-1]["tiles"]) == 7
    pass


def test_handleRequest(sample_game):
    # bug - pickRandomTile function exceeds recursion limit for more than 2 players
    # result = sample_game.handleRequest({ "request" : "setup", "players" : ["A", "B"] })
    result1 = sample_game.handleRequest(
        {"request1": "setup", "players": ["A", "B"]})
    print(result1)
    assert result1["error"] ==  'Invalid request'


# -------------------- Tiles.py ----------------------
def test_Tiles():
    # bug - validate tiles and throw excepti
    with pytest.raises(Exception) as exc_info:
        result = Tiles(10, 50)
    assert str(exc_info.value) == "Invalid tile"

# -------------------- Hotel.py ----------------------


def test_Hotel():
    # bug - validate label
    result = Hotel("American", [
        Tiles(1, 2),
        Tiles(1, 3),
        Tiles(1, 4)
    ])
    print(result)
    assert result.label == "American"
    assert result.tiles == [
        Tiles(1, 2),
        Tiles(1, 3),
        Tiles(1, 4)
    ]
# -------------------- Player.py ----------------------


def test_Player():
    # bug - validate name, cash
    result = Player("Name", 6500, [Share("American", 2)], [
        Tiles(1, 2),
        Tiles(1, 3),
        Tiles(1, 4)
    ])
    assert result.name == "Name"

# -------------------- Share.py ----------------------


def test_Share():
    # bug - validate name and count
    result = Share("American", 20)
    assert result.name == "American"
    assert result.count == 20
    
    with pytest.raises(Exception) as exc_info:
        result1 = Share("RandomHotel", 21)
    assert str(exc_info.value) == "Invalid share name"
    
    with pytest.raises(Exception) as exc_info:
        result2 = Share("American", 100)
    assert str(exc_info.value) == "Invalid share count"

