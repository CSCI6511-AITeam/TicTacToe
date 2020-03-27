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
            return False
        if self._boardmap[y][x] != 0:
            return False
        if self._result == 0:
            if self._boardmap[y][x] != 0:
                # print('Position has captured')
                return False
            if player == 1:
                self._boardmap[y][x] = 1
            elif player == 2:
                self._boardmap[y][x] = 2
            self._pace += 1
        else:
            if end_round:
                # print('Round has ended')
                return True

        self._result = self.check_win(x, y, player)
        return True

    def get_score(self, player, my_turn):
        score = np.zeros((self._m + 1, 2), dtype=int)
        for i in range(0, self._n * self._n):
            x = i % self._n
            y = i // self._n
            if self._boardmap[y][x] != 0:
                team = self._boardmap[y][x]
                for j in range(0, 4):
                    temp = [0] * 7
                    if team == player:
                        temp[3] = player + 1
                        if temp[3] > 2:
                            temp[3] = 1
                    else:
                        temp[3] = player
                    if j == 0:
                        temp[0] = 0
                        temp[1] = self._n - 1
                        temp[2] = 1
                        temp[4] = self._n - 1
                        temp[5] = 0
                        temp[6] = -1
                    elif j == 1:
                        temp[0] = 0
                        temp[1] = self._n
                        temp[2] = 1
                        temp[4] = self._n - 1
                        temp[5] = self._n
                        temp[6] = 0
                    elif j == 2:
                        temp[0] = 0
                        temp[1] = 0
                        temp[2] = 1
                        temp[4] = self._n - 1
                        temp[5] = self._n - 1
                        temp[6] = 1
                    else:
                        temp[0] = self._n
                        temp[1] = 0
                        temp[2] = 0
                        temp[4] = self._n
                        temp[5] = self._n - 1
                        temp[6] = 1
                    if_seq = 1
                    if_block = 0
                    if_hole = -1
                    length = 1
                    last_seq = 0
                    last_block = 0
                    seq_length = 1
                    max_seq = 0
                    current_x = x
                    current_y = y
                    while True:
                        if current_y == temp[0] or current_x == temp[1] \
                                or self._boardmap[current_y-temp[2]][current_x-temp[6]] == temp[3]:
                            if current_x == x and current_y == y:
                                last_block = 1
                            break
                        current_x = current_x - temp[6]
                        current_y = current_y - temp[2]
                        if self._boardmap[current_y][current_x] == team:
                            break
                        length += 1
                    if (current_x != x or current_y != y) and self._boardmap[current_y][current_x] == team:
                        continue
                    current_x = x
                    current_y = y
                    while True:
                        if current_y == temp[4] or current_x == temp[5] \
                                or self._boardmap[current_y+temp[2]][current_x+temp[6]] == temp[3]:
                            break
                        current_x = current_x + temp[6]
                        current_y = current_y + temp[2]
                        if if_seq == 1:
                            if self._boardmap[current_y][current_x] == team:
                                seq_length += 1
                            else:
                                if_seq = 0
                                if max_seq == seq_length + last_seq and max_seq != 0:
                                    if last_block == 0:
                                        if_block = 0
                                    if if_hole == 1 and last_seq == 0:
                                        if_hole = 0
                                if max_seq < seq_length + last_seq:
                                    if_block = last_block
                                    if last_seq != 0:
                                        if_hole = 1
                                    else:
                                        if_hole = 0
                                    max_seq = seq_length + last_seq
                                last_seq = seq_length
                                seq_length = 0
                        else:
                            if self._boardmap[current_y][current_x] == team:
                                if_seq = 1
                                seq_length = 1
                            else:
                                last_seq = 0
                                last_block = 0
                        length += 1
                    if max_seq == seq_length + last_seq and max_seq != 0:
                        if if_hole == 1 and last_seq == 0:
                            if_block = 1
                            if_hole = 0
                    if max_seq < seq_length + last_seq:
                        if_block = 1
                        max_seq = seq_length + last_seq
                        if last_seq != 0:
                            if_hole = 1
                        else:
                            if_hole = 0
                    if length >= self._m:
                        if max_seq > self._m - 1 and if_hole:
                            max_seq = self._m - 1
                        if max_seq != 0:
                            if length == self._m:
                                if_block = 1
                            if max_seq - if_block > 0:
                                if if_hole == 1:
                                    score[max_seq - if_block][team - 1] += 2
                                else:
                                    score[max_seq - if_block][team - 1] += 3
                            else:
                                score[max_seq][team-1] += 1
                        if max_seq > score[0][team-1]:
                            score[0][team-1] = max_seq
        opponent = player
        player = player - 1
        if opponent > 1:
            opponent = 1
        if my_turn == 1:
            if score[0][opponent] > self._m - 2 and score[0][player] <= score[0][opponent]:
                return -100
            if score[0][opponent] == self._m - 2 and score[0][player] <= score[0][opponent] and score[self._m - 2][opponent] != 0:
                if self._m != 3:
                    return -100
        else:
            if score[0][player] > self._m - 2 and score[0][opponent] <= score[0][player]:
                return 100
            if score[0][player] == self._m - 2 and score[0][opponent] <= score[0][player] and score[self._m - 2][player] != 0:
                if self._m != 3:
                    return 100
        if score[0][opponent] == self._m:
            return -100
        if score[0][player] == self._m:
            return 100

        s = 0
        for i in range(1, self._m+1):
            if score[0][player] > score[0][opponent]:
                s = s / 4 + score[i][player] - 0.8 * score[i][opponent]
            elif score[0][player] < score[0][opponent]:
                s = s / 4 + 0.8 * score[i][player] - score[i][opponent]
            else:
                if my_turn:
                    s = s / 4 + 0.8 * score[i][player] - score[i][opponent]
                else:
                    s = s / 4 + score[i][player] - 0.8 * score[i][opponent]
        return s

    def remove(self, x, y):
        # validation check
        if not self._n > x >= 0 or not self._n > y >= 0:
            print('Invalid position')
            return False
        if self._boardmap[y][x] == 0:
            # print('Position has not captured')
            return True
        self._boardmap[y][x] = 0
        self._pace -= 1
        self._result = 0
        return True

    def check_win(self, x, y, player):
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
            return player
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
            return player
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
            return player
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
            return player
        # Draw
        if self._pace == self._n * self._n:
            return 3
        return 0

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
                        string += '- '
                    elif self._boardmap[y][x] == 1:
                        string += 'X '
                    elif self._boardmap[y][x] == 2:
                        string += 'O '
                if X == 2:
                    if self._boardmap[y][x] == 0:
                        string += '- '
                    elif self._boardmap[y][x] == 1:
                        string += 'O '
                    elif self._boardmap[y][x] == 2:
                        string += 'X '
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

    def get_n(self):
        return self._n

    def get_pace(self):
        return self._pace


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
    b.move(6, 6, 2)

    b.move(0, 0, 1)
    b.move(1, 0, 2)
    b.move(0, 1, 2)
    b.move(0, 2, 1)
    b.move(1, 2, 1)

    print(b.get_board())
    board_string = b.get_board_string()
    print(board_string)
    # b.clear_board()
    # b.read_board_string(board_string)
    # # print(b.get_board())
    # chess = b.get_chess(2, 2)
    # print(chess)
    print('winner: ', b.get_result())

# test()
