from core.board import Board
import utils.connection as con
import time

my_team = 1208

class Game:
    def __init__(self, online=True):
        self.m = 0
        self.n = 0
        self.game_id = 0
        self.team1 = my_team
        self.team2 = 0
        self.game_ready = False
        self.board = None
        self.our_team = 0
        self.adversary_team = 0
        self.current_round_team = 0
        self.move_id = None
        self.game_end = False
        self.online = online

    # Create a new game
    def create_game(self, adversary_id, board_size, target):
        try:
            if self.online:
                self.game_id = con.create_game(my_team, adversary_id, board_size, target)
            else:
                self.game_id = 0
            self.m = target
            self.n = board_size
            self.team2 = adversary_id
            self.game_ready = True
            self.board = Board(self.m, self.n)
            return True
        except Exception as e:
            print('Exception: ', e)
            print('Failed to join the game')
            return False


    # Join a game
    def join_game(self, game_id, adversary_id, board_size, target):
        self.m = target
        self.n = board_size
        self.game_id = game_id
        self.team2 = adversary_id
        if self.online:
            board_map, status = con.get_board_map(self.game_id)
        else:
            status = 'OK'
        if status == 'OK':
            self.game_ready = True
            self.board = Board(self.m, self.n)
            if self.online:
                self.board.read_board_string(board_map)
            return True
        else:
            print('Failed to join the game')
            return False


    def start(self):
        while True:
            print('TicTacToe')
            if self.online is False:
                print('[OFFLINE MODE]')
            print('------------------------------------')
            print('1.Create a new round')
            print('2.Join a round')
            print('------------------------------------')
            enter = input()
            if enter == '1':
                adversary_id = int(input('Enter adversary team id:'))
                board_size = int(input('Enter board size:'))
                target = int(input('Enter win target:'))
                while True:
                    chess = input('We are:[X/O]')
                    if chess == 'X':
                        self.our_team = 1
                        self.adversary_team = 2
                        break
                    elif chess == 'O':
                        self.our_team = 2
                        self.adversary_team = 1
                        break
                    else:
                        print('Invalide input.')
                if self.create_game(adversary_id, board_size, target):
                    print(self.board.get_board_string())
                    break
                else:
                    print('Failed to start')
            elif enter == '2':
                game_id = int(input('Enter the game id you want to join:'))
                adversary_id = int(input('Enter adversary team id:'))
                board_size = int(input('Enter board size:'))
                target = int(input('Enter win target:'))
                while True:
                    chess = input('We are:[X/O]')
                    if chess == 'X':
                        self.our_team = 1
                        self.adversary_team = 2
                        break
                    elif chess == 'O':
                        self.our_team = 2
                        self.adversary_team = 1
                        break
                    else:
                        print('Invalide input.')
                if self.join_game(game_id, adversary_id, board_size, target):
                    # self.board.read_board_string(con.get_board_string(game_id))
                    print(self.board.get_board_string())
                    break
                else:
                    print('Failed to start')
            else:
                print('Invalid input.')
        while True:
            first = input('Who first? [X/O] Notice: For now API force the first player is O, so must be O.\n')
            if first == 'X':
                self.current_round_team = 1
                break
            elif first == 'O':
                self.current_round_team = 2
                break
            else:
                print('Invalid input.')

        while self.update():
            pass


    def update(self):
        if self.current_round_team == self.our_team:
            self.our_turn()
        elif self.current_round_team == self.adversary_team:
            self.adversary_turn(ai=True)
        if self.game_end:
            print('Round end')
            return False
        return True

    def next_team(self):
        self.current_round_team += 1
        if self.current_round_team > 2:
            self.current_round_team = 1

    def our_turn(self):
        while True:
            # Use AI to replace this section.
            # -----------------------------------------------------------------------------------
            x, y = str.split(input('Enter move position (left up is 1 1): \"x y\"\n'), ' ')
            x = int(x) - 1
            y = int(y) - 1
            # -----------------------------------------------------------------------------------
            pos = [x, y]
            if self.online:
                self.move_id = con.move(self.game_id, self.team1, pos)
            else:
                self.move_id = 0
            if self.move_id is None:
                print('Failed to move, please try again.')
                continue
            if self.board.move(x, y, self.current_round_team):
                break
            else:
                print('Please move again.')
        print(self.board.get_board_string())
        print(self.board.get_result())
        if self.online:
            # DEBUG
            # print(con.get_board_string(self.game_id))
            pass
        if self.board.get_result() == self.our_team:
            print('We win!')
            self.game_end = True
        elif self.board.get_result() == self.adversary_team:
            print('We lose.')
            self.game_end = True
        elif self.board.get_result() == 3:
            print('Draw.')
            self.game_end = True
        self.next_team()

    def adversary_turn(self, ai=False):
        if ai is False:
            print('Waiting for response...')
            while True:
                move = con.get_moves(self.game_id, 1)
                if move is None:
                    print('Failed to get move.')
                    time.sleep(1)
                    continue
                move = move[0]
                if int(move['moveId']) == self.move_id:
                    time.sleep(1)
                else:
                    x = int(move['moveX'])
                    y = int(move['moveY'])
                    self.board.move(x, y, self.current_round_team)
                    break
            print(self.board.get_board_string())
            self.next_team()
        else:
            # For test
            while True:
                # Use AI to replace this section.
                # -----------------------------------------------------------------------------------
                x, y = str.split(input('Enter move position (left up is 1 1): \"x y\"\n'), ' ')
                x = int(x) - 1
                y = int(y) - 1
                # -----------------------------------------------------------------------------------
                pos = [x, y]
                if self.online:
                    self.move_id = con.move(self.game_id, self.team2, pos)
                else:
                    self.move_id = 0
                if self.move_id is None:
                    print('Failed to move, please try again.')
                    continue
                if self.board.move(x, y, self.current_round_team):
                    break
                else:
                    print('Please move again.')
            print(self.board.get_board_string())
            print(self.board.get_result())
            if self.online:
                # DEBUG
                # print(con.get_board_string(self.game_id))
                pass
            if self.board.get_result() == self.adversary_team:
                print('We win!')
                self.game_end = True
            elif self.board.get_result() == self.our_team:
                print('We lose.')
                self.game_end = True
            elif self.board.get_result() == 3:
                print('Draw.')
                self.game_end = True
            self.next_team()
            pass