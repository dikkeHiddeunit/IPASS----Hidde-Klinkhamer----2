from game_state import board, board_status


ai = 1
player = -1
def small_board_check_winner(small_board):
    # Check winning rows
    if small_board[0] == small_board[1] == small_board[2] != 0:
        return small_board[0]
    if small_board[3] == small_board[4] == small_board[5] != 0:
        return small_board[3]
    if small_board[6] == small_board[7] == small_board[8] != 0:
        return small_board[6]

    # Check winning columns
    if small_board[0] == small_board[3] == small_board[6] != 0:
        return small_board[0]
    if small_board[1] == small_board[4] == small_board[7] != 0:
        return small_board[1]
    if small_board[2] == small_board[5] == small_board[8] != 0:
        return small_board[2]

    # Check winning diagonals
    if small_board[0] == small_board[4] == small_board[8] != 0:
        return small_board[0]
    if small_board[2] == small_board[4] == small_board[6] != 0:
        return small_board[2]

    return 0


def small_board_is_full(small_board_index):
    small_board = board[small_board_index]
    for x in small_board:
        if x == 0:
            return False
    board_status[small_board_index] = -1
    return True

def change_frame_button_color(buttons, frame_index, winner):
    buttons_in_frame = buttons[frame_index]

    if winner == "X":
        for button in buttons_in_frame:
            button.config(bg="tomato")
    elif winner == "draw":
        for button in buttons_in_frame:
            button.config(bg="yellow")
    elif winner == "O":
        for button in buttons_in_frame:
            button.config(bg="cornflowerblue")

def small_board_check(buttons, small_board_index):
    small_board = board[small_board_index]
    win = small_board_check_winner(small_board)
    if win == 1:
        winner = "O"
    if win == -1:
        winner = "X"
    full = small_board_is_full(small_board_index)
    if win != 0:
        change_frame_button_color(buttons, small_board_index, winner)
        board_status[small_board_index] = -1
        return win
    elif full is True:
        change_frame_button_color(buttons, small_board_index, "draw")
        board_status[small_board_index] = -1
        return full
    else:
        return None

def small_board_winning_move(small_board, player):
    # Check winning rows
    for i in range(0, 9, 3):
        if small_board[i] == small_board[i + 1] == player and small_board[i + 2] == 0:
            return i + 2
        elif small_board[i] == small_board[i + 2] == player and small_board[i + 1] == 0:
            return i + 1
        elif small_board[i + 1] == small_board[i + 2] == player and small_board[i] == 0:
            return i

    # Check winning columns
    for i in range(3):
        if small_board[i] == small_board[i + 3] == player and small_board[i + 6] == 0:
            return i + 6
        elif small_board[i] == small_board[i + 6] == player and small_board[i + 3] == 0:
            return i + 3
        elif small_board[i + 3] == small_board[i + 6] == player and small_board[i] == 0:
            return i

    # Check winning diagonals
    if small_board[0] == small_board[4] == player and small_board[8] == 0:
        return 8
    elif small_board[0] == small_board[8] == player and small_board[4] == 0:
        return 4
    elif small_board[4] == small_board[8] == player and small_board[0] == 0:
        return 0
    elif small_board[2] == small_board[4] == player and small_board[6] == 0:
        return 6
    elif small_board[2] == small_board[6] == player and small_board[4] == 0:
        return 4
    elif small_board[4] == small_board[6] == player and small_board[2] == 0:
        return 2

    # No winning move
    return None

def small_board_evaluate(small_board):
    x3 = small_board_count(small_board, -1, 3)
    x2 = small_board_count(small_board, -1, 2)
    x1 = small_board_count(small_board, -1, 1)
    o3 = small_board_count(small_board, 1, 3)
    o2 = small_board_count(small_board, 1, 2)
    o1 = small_board_count(small_board, 1, 1)

    value = (10 * o3 + 3 * o2 + o1) - (10 * x3 + 3 * x2 + x1)
    return value

def small_board_count(small_board, player, n):
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
    small_board = board[small_board_index]
    total_board_evaluation = []
    score = 0
    multi = [1.4, 1, 1.4, 1, 1.75, 1, 1.4, 1, 1.4] #https://github.com/zesardine/UltimateTicTacToeAI
    for x in range(9):
        if x == small_board_index:
            score += small_board_evaluate(small_board) * multi[x]
        else:
            score += small_board_evaluate(board[x]) * 1.5 * multi[x]
        win = small_board_check_winner(board[x])
        score += win * multi[x]
        total_board_evaluation.append(win)

    # Evaluatie van het totale bord
    total_win = small_board_check_winner(total_board_evaluation)
    score += 10000 * total_win

    # Controleer of er een winnende zet is voor de AI
    winning_move = small_board_winning_move(small_board, ai)
    if winning_move is not None:
        score += 500

    return score



def get_available_moves(board, small_board_index):
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
    if total_board_evaluate(small_board_index) > 100000 or depth <= 0:
        return total_board_evaluate(small_board_index), None

    available_moves = get_available_moves(board, small_board_index)

    if maximizing:
        best_score = float('-inf')
        best_play = None
        for move in available_moves:
            board[move[0]][move[1]] = ai
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
            board[move[0]][move[1]] = player
            score, _ = minimax(board, move[1], depth - 1, alpha, beta, True)
            board[move[0]][move[1]] = 0
            if score < best_score:
                best_score = score
                best_play = move
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        return best_score, best_play
