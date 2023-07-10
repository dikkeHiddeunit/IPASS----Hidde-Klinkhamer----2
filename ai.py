from game_state import board, board_status, frame_winner

AI = 1
PLAYER = -1


def small_board_check_winner(small_board):
    """Checks if there is a winner in a small board.
    Args:
        small_board (list): The small board to check.
    Returns:
        int: The winner: AI, PLAYER, or 0 (no winner).
    """
    for i in range(0, 9, 3):
        if small_board[i] == small_board[i + 1] == small_board[i + 2] != 0:
            return small_board[i]

    # Checks winning columns
    for i in range(3):
        if small_board[i] == small_board[i + 3] == small_board[i + 6] != 0:
            return small_board[i]

    # Checks winning diagonals
    if small_board[0] == small_board[4] == small_board[8] != 0:
        return small_board[0]
    if small_board[2] == small_board[4] == small_board[6] != 0:
        return small_board[2]

    return 0

def small_board_is_full(small_board_index):
    """Checks if a small board is full.
    Args:
        small_board_index (int): The index of the small board.
    Returns:
        bool: True if the small board is full, False otherwise.
    """
    return all(cell != 0 for cell in board[small_board_index])

def change_frame_button_color(buttons, frame_index, winner):
    """Changes the color of buttons in a frame based on the winner.
    Args:
        buttons (list): The list of buttons.
        frame_index (int): The index of the frame.
        winner (int): The winner: AI, PLAYER, or 0 (no winner).
    """
    buttons_in_frame = buttons[frame_index]

    if winner == AI:
        color = "cornflowerblue"
    elif winner == PLAYER:
        color = "tomato"
    else:
        color = "yellow"

    for button in buttons_in_frame:
        button.config(bg=color)

def small_board_check(buttons, small_board_index):
    """Checks the status of a small board (winner, full, or no winner).
    Args:
        buttons (list): The list of buttons.
        small_board_index (int): The index of the small board.
    Returns:
        int or None: The winner: AI or PLAYER, or full if the small board is full. None if there is no winner or full.
    """
    small_board = board[small_board_index]
    win = small_board_check_winner(small_board)
    if win == AI:
        frame_winner[small_board_index] = PLAYER
    elif win == PLAYER:
        frame_winner[small_board_index] = AI

    full = small_board_is_full(small_board_index)
    if win != 0:
        change_frame_button_color(buttons, small_board_index, win)
        board_status[small_board_index] = -1
        return win
    elif full:
        change_frame_button_color(buttons, small_board_index, "draw")
        board_status[small_board_index] = -1
        return full
    else:
        return None

def small_board_evaluate(small_board):
    """Evaluates a small board for AI.
    Args:
        small_board (list): The small board to evaluate.
    Returns:
        int: The evaluation score.
    """
    x3 = small_board_count(small_board, -1, 3)
    x2 = small_board_count(small_board, -1, 2)
    x1 = small_board_count(small_board, -1, 1)
    o3 = small_board_count(small_board, 1, 3)
    o2 = small_board_count(small_board, 1, 2)
    o1 = small_board_count(small_board, 1, 1)

    value = (10 * o3 + 3 * o2 + o1) - (10 * x3 + 3 * x2 + x1)
    return value

def small_board_count(small_board, player, n):
    """Counts the occurrences of a player's moves in a small board.
    Args:
        small_board (list): The small board to count.
        player (int): The player: AI or PLAYER.
        n (int): The number of moves to count.
    Returns:
        int: The count of occurrences.
    """
    count = 0

    # Check horizontal rows
    for i in range(3):
        row = small_board[i * 3: (i + 1) * 3]
        if row.count(player) == n and row.count(0) == 3 - n:
            count += 1

    # Check vertical columns
    for i in range(3):
        column = [small_board[i], small_board[i + 3], small_board[i + 6]]
        if column.count(player) == n and column.count(0) == 3 - n:
            count += 1

    # Check diagonals
    diagonal1 = [small_board[0], small_board[4], small_board[8]]
    diagonal2 = [small_board[2], small_board[4], small_board[6]]
    if diagonal1.count(player) == n and diagonal1.count(0) == 3 - n:
        count += 1
    if diagonal2.count(player) == n and diagonal2.count(0) == 3 - n:
        count += 1

    return count

def total_board_evaluate(small_board_index):
    """Evaluates the total board for AI.
    Args:
        small_board_index (int): The index of the small board.
    Returns:
        int: The evaluation score.
    """
    small_board = board[small_board_index]
    total_board_evaluation = []
    score = 0
    multi = [1.4, 1, 1.4, 1, 1.75, 1, 1.4, 1, 1.4] # Taken from https://github.com/zesardine/UltimateTicTacToeAI
    for x in range(9):
        if x == small_board_index:
            score += small_board_evaluate(small_board) * multi[x]
        else:
            score += small_board_evaluate(board[x]) * 1.5 * multi[x]
        win = small_board_check_winner(board[x])
        score += win * multi[x]
        total_board_evaluation.append(win)

    # Evaluation of the total board
    total_win = small_board_check_winner(total_board_evaluation)
    score += 10000 * total_win

    return score

def get_available_moves(board, small_board_index):
    """Gets the available moves in a small board or any board.
    Args:
        board (list): The game board.
        small_board_index (int): The index of the small board.
    Returns:
        list: The list of available moves as (small_board_index, move_index) tuples.
    """
    available_moves = []

    if board_status[small_board_index] == 0:
        for x in range(9):
            if board[small_board_index][x] == 0:
                available_moves.append((small_board_index, x))
    else:
        for x in range(9):
            if board_status[x] == 0:
                for y in range(9):
                    if board[x][y] == 0:
                        available_moves.append((x, y))

    return available_moves

def minimax(board, small_board_index, depth, alpha, beta, maximizing):
    """Minimax algorithm with alpha-beta pruning.
    Args:
        board (list): The game board.
        small_board_index (int): The index of the small board.
        depth (int): The depth of the search.
        alpha (float): The alpha value for alpha-beta pruning.
        beta (float): The beta value for alpha-beta pruning.
        maximizing (bool): True if maximizing the AI's score, False if minimizing the player's score.
    Returns:
        tuple: The best score and the best play as (score, play) tuple.
    """
    if depth == 0 or small_board_is_full(small_board_index):
        return total_board_evaluate(small_board_index), None

    available_moves = get_available_moves(board, small_board_index)

    if maximizing:
        best_score = float('-inf')
        best_play = None
        for move in available_moves:
            board[move[0]][move[1]] = AI
            score, _ = minimax(board, move[1], depth - 1, alpha, beta, False)
            board[move[0]][move[1]] = 0
            if score > best_score:
                best_score = score
                best_play = move
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score, best_play
    else:
        best_score = float('inf')
        best_play = None
        for move in available_moves:
            board[move[0]][move[1]] = PLAYER
            score, _ = minimax(board, move[1], depth - 1, alpha, beta, True)
            board[move[0]][move[1]] = 0
            if score < best_score:
                best_score = score
                best_play = move
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score, best_play


board = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, -1, 0, 0, -1, 0, 0, 0, -1],
    [1, 1, 1, -1, 0, 0, 0, 0, -1],
    [-1, -1, -1, 0, 1, 0, 0, 0, 1],
    [0, 0, 0, 1, -1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1]
]
print(small_board_evaluate([board[2]]))