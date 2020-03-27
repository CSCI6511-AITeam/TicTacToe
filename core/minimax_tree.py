

# Use Node(player, score, x, y) to init the node.
class Node:
    def __init__(self):
        self._root = None
        self._player = 0
        self._score = None
        self._alpha = None
        self._beta = None
        self._no = None
        self._childs = []
        self._child_amount = 0
        self._pos = []
        pass

    def __init__(self, player, score, x, y):
        self._root = None
        self._player = player
        self._score = score
        self._alpha = None
        self._beta = None
        self._no = None
        self._pos = [x, y]
        self._childs = []
        self._child_amount = 0
        pass

    def set_root(self, root):
        self._root = root

    def add_child(self, node):
        node.set_no(self._child_amount)
        self._child_amount += 1
        node.set_root(self)
        self._childs.append(node)

    def set_player(self, player):
        self._player = player

    def set_score(self, score):
        self._score = score

    def set_pos(self, x, y):
        self._pos = [x, y]

    def set_alpha(self, a):
        self._alpha = a

    def set_beta(self, b):
        self._beta = b

    def set_no(self, no):
        self._no = no

    def get_score(self):
        return self._score

    def get_alpha_beta(self):
        return self._alpha, self._beta

    def get_player(self):
        return self._player

    def get_pos(self):
        return self._pos

    def get_childs_list(self):
        return self._childs

    def get_root(self):
        return self._root

    def get_no(self):
        return self._no

    def get_child_amount(self):
        return self._child_amount


# Introduction
#   Use MinimaxTree(head_node) to init the tree
#   Pointer will point to the head node
#   ALL OPERATIONS BASE ON POINTER
#
#   Method:
# -------------------------------------------------------------------------------------------------------------------
#   Pointer Control:
#   get_pointed_node()      Get the current pointed node
#                               Return: Current pointer (node)
#   go_head()               Go to head node
#                               Return: Head node
#   go_neighbor()           Go to neighbor node at the same depth and under the same root
#                               Return: Neighbor node or None(if no neighbor)
#   go_first_child()        Go to the first child node of the current pointed node
#                               Return: First child node or None(if no child)
#   go_root()               Go to the root node of the current pointed node
#                               Return: Root node
# -------------------------------------------------------------------------------------------------------------------
#   add_child(Node)         Add a child node to the current pointed node
#   begin_search            Use this when evaluation of the score begin.
#                               pointer will go to the first node that needed to be evaluated.
#                               Return: First node to evaluate
#   next()                  Go to the next node that needed to be evaluated.
#                               Return: Next node or None(Reach the end)
#   get_new_chess()         Get all new chess when reach the current pointed node.
#                               Return: [[player, [x, y]], ...]
class MinimaxTree:
    def __init__(self, head_node):
        self._head = head_node
        self._head: Node
        self._pointer = head_node
        self._head_player = self._pointer.get_player()

    # Go to the head node
    def go_head(self):
        self._pointer = self._head
        return self._pointer

    # Go to the previous node
    def go_root(self):
        if self._pointer.get_root() is not None:
            self._pointer = self._pointer.get_root()
            return self._pointer
        else:
            # print("Head node already")
            return None

    # Go to the next neighbor
    def go_neighbor(self):
        current_no = self._pointer.get_no()
        previous_node = self._pointer
        self._pointer = self._pointer.get_root()
        if current_no + 1 < self._pointer.get_child_amount():
            self._pointer = self._pointer.get_childs_list()[current_no + 1]
            return self._pointer
        else:
            # print("No more neighbor")
            self._pointer = previous_node
            return None

    # Go to the next neighbor with a b score calculation
    def go_neighbor_cal(self):
        current_no = self._pointer.get_no()
        root = self._pointer.get_root()
        if root is None:
            # Has reached the last possible node and end in the head node
            # print("Reach the end")
            return None
        root: Node
        root_player = root.get_player()
        root_alpha, root_beta = root.get_alpha_beta()
        score = self._pointer.get_score()
        # alpha
        if root_player == self._head_player:
            if root_alpha is None or score > root_alpha:
                root.set_alpha(score)
                root_alpha = score
            # score
            if root.get_score() is None or score > root.get_score():
                root.set_score(score)
        # beta
        else:
            if root_beta is None or score < root_beta:
                root.set_beta(score)
                root_beta = score
            # score
            if root.get_score() is None or score < root.get_score():
                root.set_score(score)
        if root_alpha is not None and root_beta is not None:
            if root_alpha >= root_beta:
                return None

        previous_node = self._pointer
        self._pointer = root
        if current_no + 1 < self._pointer.get_child_amount():
            self._pointer = self._pointer.get_childs_list()[current_no + 1]
            # if root_player == self._head_player:
            #     self._pointer.set_alpha(root.get_alpha_beta()[0])
            # else:
            #     self._pointer.set_beta(root.get_alpha_beta()[1])
            self._pointer.set_alpha(root.get_alpha_beta()[0])
            self._pointer.set_beta(root.get_alpha_beta()[1])
            return self._pointer
        else:
            # print("No more neighbor")
            self._pointer = previous_node
            return None

    # Go to the first child
    def go_first_child(self):
        if self._pointer.get_childs_list():
            self._pointer = self._pointer.get_childs_list()[0]
            return self._pointer
        else:
            # print("No more child")
            return None

    def begin_search(self):
        self.go_head()
        while self.go_first_child() is not None:
            pass
        return self._pointer

    # Automatically select the next node to be evaluated according to pruning.
    # Use begin_search() before using it.
    # Return None if ended. Pointer will go to the head node
    # Calculate the pointer node score after using this
    def next(self):
        root = self._pointer.get_root()
        if root is None:
            return None
        root: Node
        score = self._pointer.get_score()
        root_alpha, root_beta = root.get_alpha_beta()
        root_player = root.get_player()

        # alpha
        if root_player == self._head_player:
            if root_alpha is None or score > root_alpha:
                root.set_alpha(score)
                root_alpha = score
            # score
            if root.get_score() is None or score > root.get_score():
                root.set_score(score)
        # beta
        else:
            if root_beta is None or score < root_beta:
                root.set_beta(score)
                root_beta = score
            # score
            if root.get_score() is None or score < root.get_score():
                root.set_score(score)

        # alpha <= N <= beta
        if self.go_neighbor() is None or \
                ((root_alpha is not None and root_beta is not None) and (root_alpha >= root_beta)):
            while True:
                if self.go_root():
                    if self.go_neighbor_cal():
                        while self.go_first_child():
                            root = self._pointer.get_root()
                            root: Node
                            # if self._pointer.get_player() == self._head_player:
                            #     self._pointer.set_beta(root.get_alpha_beta()[1])
                            # else:
                            #     self._pointer.set_alpha(root.get_alpha_beta()[0])
                            self._pointer.set_beta(root.get_alpha_beta()[1])
                            self._pointer.set_alpha(root.get_alpha_beta()[0])
                        return self._pointer
                else:
                    # Ended at the head node
                    return None
        else:
            return self._pointer

    # Add child to the current pointer
    def add_child(self, node):
        self._pointer.add_child(node)

    def get_pointer_node(self):
        return self._pointer

    # Get all new chess when reach current node
    def get_new_chess(self):
        current_point = self._pointer
        new_chess = []
        while True:
            self._pointer: Node
            pos = self._pointer.get_pos()
            player = self._pointer.get_player()
            new_chess.append([player, pos])
            if self.go_root() is None:
                break
        self._pointer = current_point
        return new_chess

    def get_next_move(self):
        current_point = self._pointer
        self.go_head()
        self.go_first_child()
        # print(self.get_pointer_node().get_score())
        best_score = self.get_pointer_node().get_score()
        best_pos = self.get_pointer_node().get_pos()
        while self.go_neighbor() is not None:
            # print(self.get_pointer_node().get_score())
            if self.get_pointer_node().get_score() > best_score:
                best_score = self.get_pointer_node().get_score()
                best_pos = self.get_pointer_node().get_pos()
        self._pointer = current_point
        return best_pos


def test():
    head_node = Node(2, None, -1, -1)
    head_node.set_no(0)
    tree = MinimaxTree(head_node)
    node = Node(1, None, 0, 1)
    tree.add_child(node)
    node = Node(1, None, 1, 1)
    tree.add_child(node)

    tree.go_first_child()
    node = Node(2, None, 0, 2)
    tree.add_child(node)
    node = Node(2, None, 1, 2)
    tree.add_child(node)

    tree.go_neighbor()
    node = Node(2, None, 2, 2)
    tree.add_child(node)
    node = Node(2, None, 3, 2)
    tree.add_child(node)

    tree.go_root()
    tree.go_first_child()
    tree.go_first_child()

    node = Node(1, None, 0, 3)
    tree.add_child(node)
    node = Node(1, None, 1, 3)
    tree.add_child(node)

    tree.go_neighbor()
    node = Node(1, None, 2, 3)
    tree.add_child(node)
    node = Node(1, None, 3, 3)
    tree.add_child(node)

    tree.go_head()
    tree.go_first_child()
    tree.go_neighbor()
    tree.go_first_child()
    node = Node(1, None, 4, 3)
    tree.add_child(node)
    node = Node(1, None, 5, 3)
    tree.add_child(node)

    tree.go_neighbor()
    node = Node(1, None, 6, 3)
    tree.add_child(node)

    tree.go_head()
    tree.go_first_child()
    tree.go_first_child()
    tree.go_first_child()
    node = Node(2, 3, 0, 4)
    tree.add_child(node)
    node = Node(2, 17, 1, 4)
    tree.add_child(node)

    tree.go_neighbor()
    node = Node(2, 2, 2, 4)
    tree.add_child(node)
    node = Node(2, 0, 3, 4)
    tree.add_child(node)

    tree.go_root()
    tree.go_neighbor()
    tree.go_first_child()
    node = Node(2, 15, 4, 4)
    tree.add_child(node)
    tree.go_neighbor()
    node = Node(2, 0, 5, 4)
    tree.add_child(node)
    node = Node(2, 0, 6, 4)
    tree.add_child(node)

    tree.go_head()
    tree.go_first_child()
    tree.go_neighbor()
    tree.go_first_child()
    tree.go_first_child()
    node = Node(2, 2, 7, 4)
    tree.add_child(node)
    node = Node(2, 0, 8, 4)
    tree.add_child(node)
    tree.go_neighbor()
    node = Node(2, 4, 9, 4)
    tree.add_child(node)
    tree.go_root()
    tree.go_neighbor()
    tree.go_first_child()
    node = Node(2, 0, 10, 4)
    tree.add_child(node)
    node = Node(2, 0, 11, 4)
    tree.add_child(node)

    tree.go_head()
    tree.go_first_child()
    tree.go_first_child()
    tree.go_first_child()
    tree.go_first_child()
    tree.go_neighbor()
    tree.go_neighbor()

    tree.go_root()
    tree.go_neighbor()
    tree.go_first_child()
    tree.go_neighbor()

    tree.begin_search()
    while tree.next() is not None:
        pass

    print("\n")
    tree.go_head()
    tree.go_first_child()
    print(tree.get_next_move())

    print(tree.get_pointer_node().get_score())
    print(tree.get_new_chess())
    print(tree.get_pointer_node().get_score())

    # print(tree.get_pointer_node().get_pos())
    # print(tree.get_pointer_node().get_alpha_beta())


#test()
