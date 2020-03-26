import json
import requests
import urllib
import ast

url = 'https://www.notexponential.com/aip2pgaming/api/index.php'

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        "x-api-key": "2bcbdd8198006bf2d68f",
        "userId": "853"
    }


# Return game ID
def create_game(team1, team2, boardsize, target):
    data = {
        "type": "game",
        "teamId1": team1,
        "teamId2": team2,
        "gameType": "TTT",
        "boardSize": boardsize,
        "target": target
    }
    try:
        response = requests.post(url, data=data, headers=headers)
        print(response.text)
        dict = ast.literal_eval(response.text)
        gameId = int(dict['gameId'])
        return gameId
    except Exception as e:
        print('Connection failed')
        print(e)
        return None


# Pos=[x, y]. Return move ID
def move(game_id, team_id, pos):
    pos_str = '' + str(pos[1]) + ',' + str(pos[0])
    data = {
        "type": "move",
        "gameId": game_id,
        "teamId": team_id,
        "move": pos_str
    }
    try:
        response = requests.post(url, data=data, headers=headers)
        print(response.text)
        dict = ast.literal_eval(response.text)
        moveId = int(dict['moveId'])
        return moveId
    except Exception as e:
        print('Connection failed')
        print(e)
        return None


# Count=How many moves from recent to show
# Return a list of moves
def get_moves(game_id, count):
    params = {
        "type": "moves",
        "gameId": game_id,
        "count": count
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        # print(response.text)
        dict = ast.literal_eval(response.text)
        moves = dict['moves']
        return moves
    except Exception as e:
        print('Connection failed')
        print(e)
        return None

# Return a board string
def get_board_string(game_id):
    params = {
        "type": "boardString",
        "gameId": game_id,
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        print(response.text)
        dict = ast.literal_eval(response.text)
        board_str = dict['output']
        return board_str
    except Exception as e:
        print('Connection failed')
        print(e)
        return None


# Return a dictionary of moves
# Testing connection availability
def get_board_map(game_id):
    params = {
        "type": "boardMap",
        "gameId": game_id,
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        print(response.text)
        dict = ast.literal_eval(response.text)
        board_map = dict['output']
        status = dict['code']
        borad_map_dict = ast.literal_eval(board_map)
        return borad_map_dict, status
    except Exception as e:
        print(e)
        print('Connection failed')
        return None, False

def test():
    # print(create_game(1208, 1208, 16, 5))
    # print(move(94, 1208, [0, 0]))
    # print(get_moves(94, 1))
    # print(get_board_string(94))
    # print(get_board_map(94))
    pass

# test()