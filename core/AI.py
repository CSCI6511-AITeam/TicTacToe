from core.board import Board
from core.minimax_tree import MinimaxTree, Node

import time;


class Ai:
    def __init__(self):
        self.team = None
        self.loop_num = 3
        pass

    def move(self, b, player):
        b: Board
        if b.get_result() != 0:
            print("game is over")
            return 0
        if b.get_pace() + self.loop_num > b.get_n() * b.get_n():
            self.loop_num = b.get_n() * b.get_n() - b.get_pace()
        start = time.time()
        tree = self.make_tree(b, player)
        tree.begin_search()
        # print(tree.get_new_chess())
        while tree.next(b, self.team, self.loop_num) is not None:
            pass
        end = time.time()
        print(end - start)
        return tree.get_next_move()

    def make_tree(self, b, player):
        self.team = player
        opponent = player + 1
        if opponent > 2:
            opponent = 1
        head_node = Node(opponent, None, -1, -1)
        head_node.set_no(0)
        tree = MinimaxTree(head_node)
        self.make_sub_tree(b, opponent, tree, 1)
        return tree

    def make_sub_tree(self, b, player, tree, loop_time):
        opponent = player + 1
        if opponent > 2:
            opponent = 1
        n = b.get_n()
        child_num = 0
        min_i, max_i = b.get_square()
        # print(min_i, max_i)
        for i in range(min_i, max_i):
            if b.move(i % n, i // n, opponent):
                if loop_time >= self.loop_num:
                    node = Node(opponent, None, i % n, i // n)
                    # print(b.get_score(self.team, loop_time % 2))
                    tree.add_child(node)
                    # get score
                    pass
                else:
                    node = Node(opponent, None, i % n, i // n)
                    tree.add_child(node)
                    tree.go_child_num(child_num)
                    child_num += 1
                    self.make_sub_tree(b, opponent, tree, loop_time + 1)
                    tree.go_root()
                b.remove(i % n, i // n)
                pass
        pass


def ai_test():
    b = Board(5, 15)
    ai = Ai()
    # b.move(1, 1, 1)
    # print(b.get_board())
    while True:
        x, y = str.split(input('Enter move position (left up is 0 0): \"x y\"\n'), ' ')
        x = int(x)
        y = int(y)
        b.move(x, y, 2)
        if b.get_result() != 0:
            print(b.get_board())
            print(b.get_result())
            break
        # print(b.get_board())
        x, y = ai.move(b, 1)
        b.move(x, y, 1)
        print(b.get_board())
        if b.get_result() != 0:
            print(b.get_board())
            print(b.get_result())
            break

'''    
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
'''


ai_test()
