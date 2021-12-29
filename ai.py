"""
Tic Tac Toe Player
"""

# AI DOESN'T IMPLEMENT ALPHA-BETA PRUNING

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # board is a two-dimensional array like the one returned by initial_state()

    xCount = 0
    oCount = 0
    emptySquares = 0

    if winner(board): # if someone won, it's no one's turn!
        return None
    else:
        for array in board:
            for item in array:
                if item == X:
                    xCount += 1
                elif item == O:
                    oCount += 1
                else:
                    emptySquares += 1

        if emptySquares == 0: # if draw, it's no one's turn!
            return None
        elif xCount > oCount:
            return O
        else:
            return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # board is a two-dimensional array like the one returned by initial_state()

    # return None if the board is terminal (has no additional possible actions)
    if player(board) is None:
        return None
    else:
        result = set()
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == EMPTY:
                    result.add((i, j))
        return result


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if action not in actions(board):
        raise ValueError('Invalid action!')
    else:
        result_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range(len(board)):
            for j in range(len(board[i])):
                result_board[i][j] = board[i][j]
        player_sign = player(board)
        result_board[action[0]][action[1]] = player_sign
        return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # check the board row-by-row then column-by-column then the two diagonals for a winning triple
    # if a winning triple is found at any point during the search, return immediately!

    # row-by-row check:
    found_triple = True
    for i in range(len(board)):
        c_sign = board[i][0]  # the first sign which will determine whether the row is a winning row or not
        for j in range(len(board[i])):
            if board[i][j] != c_sign:
                found_triple = False
                break
        if found_triple:
            return c_sign
        else:
            found_triple = True

    # column-by-column check:
    found_triple = True
    for j in range(len(board[0])):
        c_sign = board[0][j]  # the first sign which will determine whether the column is a winning column or not
        for i in range(len(board)):
            if board[i][j] != c_sign:
                found_triple = False
                break
        if found_triple:
            return c_sign
        else:
            found_triple = True

    # checking the diagonals:
    c_sign = board[1][1]  # the sign of the middle square because any diagonal must pass through the middle square

    # 1st diagonal check (upper left => bottom right):
    if board[0][0] == c_sign == board[2][2]:
        return c_sign

    # 2nd diagonal check (bottom left => upper right):
    if board[2][0] == c_sign == board[0][2]:
        return c_sign

    # if there is no winner due to any reason, return None
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # the only two ways in which a game can end are: 1. a player has won the game & 2. a tie has occurred
    # if none of the previous conditions was met, the game MUST still be going on

    if not player(board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    if terminal(board):
        return None
    else:
        answers = list()
        if player(board) == X:  # try to maximize the next move
            for action in actions(board):
                answers.append([minimize(result(board, action)), action])
            max = float('-inf')
            max_index = None
            for i in range(len(answers)):
                if answers[i][0] > max:
                    max = answers[i][0]
                    max_index = i
            return answers[max_index][1]
        else:  # try to minimize the next move
            for action in actions(board):
                answers.append([maximize(result(board, action)), action])
            min = float('inf')
            min_index = None
            for i in range(len(answers)):
                if answers[i][0] < min:
                    min = answers[i][0]
                    min_index = i
            return answers[min_index][1]


def maximize(board):
    if terminal(board):
        return utility(board)
    else:
        v = float('-inf')
        for action in actions(board):
            v = max(v, minimize(result(board, action)))
        return v


def minimize(board):
    if terminal(board):
        return utility(board)
    else:
        v = float('inf')
        for action in actions(board):
            v = min(v, maximize(result(board, action)))
        return v
