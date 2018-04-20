EMPTY_SPACE = '_'

class State:
    def __init__(self, size = 3, board = None, move_order = ('x', 'o')):
        self.size = size
        self.board = board or tuple(tuple(EMPTY_SPACE for _ in range(size)) for _ in range(size))
        self.move_order = move_order

    def move(self, move):
        row, col = move
        board_copy = tuple(tuple(self.move_order[0] if i == row and j == col else self.board[i][j]
                                 for j in range(self.size))
                           for i in range(self.size))

        state_type = self.next_state_type(board_copy)

        return state_type(board = board_copy, 
                          move_order = (*self.move_order[1:], self.move_order[0]))

    def possible_moves(self):
        return [(row, col) for row in range(self.size) 
                           for col in range(self.size) 
                           if self.board[row][col] == EMPTY_SPACE]

    def game_over(self):
        return False

    def next_state_type(self, board):
        # Check rows
        for row in range(self.size):
            if (EMPTY_SPACE != board[row][0] and 
                all(board[row][col] == board[row][0] for col in range(self.size))):
                
                return Win

        # Check columns
        for col in range(self.size):
            if (EMPTY_SPACE != board[0][col] and 
                all(board[row][col] == board[0][col] for row in range(self.size))):
                
                return Win

        # easy diagonal
        if (EMPTY_SPACE != board[0][0] and 
            all(board[d][d] == board[0][0] for d in range(self.size))):
            return Win

        # hard diagonal
        if (EMPTY_SPACE != board[0][-1] and
            all(board[d][-(d + 1)] == board[0][-1] for d in range(self.size))):
            return Win

        if all(square != EMPTY_SPACE for row in board for square in row):
            return Tie

        return State

    def __repr__(self):
        return "\n".join(("|".join(square for square in row)) for row in self.board)

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return 31*self.size ^ hash(self.board) ^ hash(self.move_order)

    def __eq__(self, other):
        return (type(self) == type(other) and 
            self.size == other.size and 
            self.move_order == other.move_order and 
            self.board == other.board)

class EndGameState(State):
    def game_over(self):
        return True

    def possible_moves(self):
        return ["Exit"]


class Win(EndGameState):
    def __str__(self):
        return super().__str__() + "\n" + "The {}'s win!".format(self.move_order[-1])

    def response(self):
        return Loss(board=self.board)


class Loss(EndGameState):
    def __str__(self):
        return super().__str__() + "\n" + "Loss"


class Tie(EndGameState):
    def __str__(self):
        return super().__str__() + "\n" + "It's a Draw!"

    def response(self):
        return Tie(board=self.board)


def rewards(prev_state, move, new_state):
    if type(new_state) is Win:
        return 100
    # if type(new_state) is Tie:
    #     return 50
    return 0

def penalties(opp_prev_state, opp_move, opp_new_state):
    if type(opp_new_state) is Win:
        return -100
    # if type(opp_new_state) is Tie:
    #     return 50
    return 0

def initial_state():
    return State()