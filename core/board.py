import numpy as np


class Board:

    # nxn board with m chess in a row to win
    def __init__(self, m, n):
        self._m = m
        self._n = n
        self._boardmap = np.zeros((n, n), dtype=int)    # 0 = None, 1 = player1, 2 = player2
        self._pace = 0
        self._result = 0              # 0 = None, 1 = player1 win, 2 = player2 win, 3 = draw
        pass

    # put chess at x,y by player 1 or 2
    def move(self, x, y, player, end_round=True):
        # validation check
        if not self._n > x >= 0 or not self._n > y >= 0:
            print('Invalid position')
            return
        if self._result == 0:
            if self._boardmap[y][x] != 0:
                print('Position has captured')
                return
            if player == 1:
                self._boardmap[y][x] = 1
            elif player == 2:
                self._boardmap[y][x] = 2
            self._pace += 1
        else:
            if end_round:
                print('Round has ended')
                return

        # win check
            # left to right
        chess_in_row = 0
        directions = [-1, 1]
        for d in directions:
            for i in range(1, self._m):
                if self._n > x + i * d >= 0:
                    if self._boardmap[y][x + i * d] == player:
                        chess_in_row += 1
                    else:
                        break
                else:
                    break
        if chess_in_row == self._m - 1:
            self._result = player
            return
            # up to down
        chess_in_row = 0
        for d in directions:
            for i in range(1, self._m):
                if self._n > y + i * d >= 0:
                    if self._boardmap[y + i * d][x] == player:
                        chess_in_row += 1
                    else:
                        break
                else:
                    break
        if chess_in_row == self._m - 1:
            self._result = player
            return
            # left up to right down
        chess_in_row = 0
        for d in directions:
            for i in range(1, self._m):
                if self._n > x + i * d >= 0 and self._n > y + i * d >= 0:
                    if self._boardmap[y + i * d][x + i * d] == player:
                        chess_in_row += 1
                    else:
                        break
                else:
                    break
        if chess_in_row == self._m - 1:
            self._result = player
            return
            # left down to right up
        chess_in_row = 0
        for d in directions:
            for i in range(1, self._m):
                if self._n > x + i * d >= 0 and self._n > y - i * d >= 0:
                    if self._boardmap[y - i * d][x + i * d] == player:
                        chess_in_row += 1
                    else:
                        break
                else:
                    break
        if chess_in_row == self._m - 1:
            self._result = player
            return
        # Draw
        if self._pace == self._n * self._n:
            self._result = 3

    def get_board(self):
        return self._boardmap

    def clear_board(self):
        self._boardmap = np.zeros((self._n, self._n), dtype=int)
        self._result = 0
        self._pace = 0

    def get_result(self):
        return self._result

    # Return board in string, player1=X:X=1 or player1=O:X=2
    def get_board_string(self, X=1):
        string = ""
        for y in range(0, self._n):
            for x in range(0, self._n):
                if X == 1:
                    if self._boardmap[y][x] == 0:
                        string += '-'
                    elif self._boardmap[y][x] == 1:
                        string += 'X'
                    elif self._boardmap[y][x] == 2:
                        string += 'O'
                if X == 2:
                    if self._boardmap[y][x] == 0:
                        string += '-'
                    elif self._boardmap[y][x] == 1:
                        string += 'O'
                    elif self._boardmap[y][x] == 2:
                        string += 'X'
            string += '\n'
        return string

    # Read board in string, player1=X:X=1 or player1=O:X=2
    def read_board_string(self, string, X=1):
        x = 0
        y = 0
        if X == 1:
            for pos in string:
                if pos == 'X':
                    self.move(x, y, 1, end_round=False)
                    x += 1
                elif pos == 'O':
                    self.move(x, y, 2, end_round=False)
                    x += 1
                elif pos == '\n':
                    y += 1
                    x = 0
                else:
                    x += 1
        if X == 2:
            for pos in string:
                if pos == 'O':
                    self.move(x, y, 2, end_round=False)
                    x += 1
                elif pos == 'X':
                    self.move(x, y, 1, end_round=False)
                    x += 1
                elif pos == '\n':
                    y += 1
                    x = 0
                else:
                    x += 1

    # Get chess in the position x,y
    def get_chess(self, x, y):
        return self._boardmap[y][x]

def test():
    b = Board(5, 16)
    b.move(1, 1, 2)
    b.move(2, 1, 1)
    b.move(3, 1, 1)
    b.move(4, 1, 1)
    b.move(5, 1, 2)
    b.move(6, 1, 2)
    b.move(7, 1, 2)
    b.move(2, 0, 1)
    b.move(2, 2, 2)
    b.move(2, 3, 1)
    b.move(4, 0, 1)
    b.move(1, 3, 1)
    b.move(3, 3, 2)
    b.move(4, 4, 2)
    b.move(5, 5, 2)

    b.move(0, 0, 1)
    b.move(1, 0, 2)
    b.move(0, 1, 2)
    b.move(0, 2, 1)
    b.move(1, 2, 1)

    print(b.get_board())
    board_string = b.get_board_string()
    print(board_string)
    b.clear_board()
    b.read_board_string(board_string)
    # print(b.get_board())
    chess = b.get_chess(2, 2)
    print(chess)
    print('winner: ', b.get_result())

test()