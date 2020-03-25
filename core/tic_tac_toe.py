from core.board import Board
import utils.connection as con

my_team = 1208

class Game:
    def __init__(self):
        self.m = 0
        self.n = 0
        self.game_id = 0
        self.team1 = my_team
        self.team2 = 0
        self.game_ready = False

    # Create a new game
    def create_game(self, adversary_id, board_size, target):
        try:
            self.game_id = con.create_game(my_team, adversary_id, board_size, target)
            self.m = target
            self.n = board_size
            self.team2 = adversary_id
            self.game_ready = True
        except Exception as e:
            print('Exception: ', e)

    # Join a game
    def join_game(self, game_id, adversary_id, board_size, target):
        self.m = target
        self.n = board_size
        self.game_id = game_id
        self.team2 = adversary_id


    def start(self):
        while self.update():
            pass

    def update(self):
        board = Board(self.m, self.n)
