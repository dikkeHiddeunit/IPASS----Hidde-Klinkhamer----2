
board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0]]

def small_board_check_winner(small_board):
    # Controleren op winnende rijen
    if small_board[0] == small_board[1] == small_board[2] != 0:
        return small_board[0]
    if small_board[3] == small_board[4] == small_board[5] != 0:
        return small_board[3]
    if small_board[6] == small_board[7] == small_board[8] != 0:
        return small_board[6]

    # Controleren op winnende kolommen
    if small_board[0] == small_board[3] == small_board[6] != 0:
        return small_board[0]
    if small_board[1] == small_board[4] == small_board[7] != 0:
        return small_board[1]
    if small_board[2] == small_board[5] == small_board[8] != 0:
        return small_board[2]

    # Controleren op winnende diagonalen
    if small_board[0] == small_board[4] == small_board[8] != 0:
        return small_board[0]
    if small_board[2] == small_board[4] == small_board[6] != 0:
        return small_board[2]
    else:
        return 0

def small_board_winning_move(small_board, player):
    # Controleer op winnende rijen
    for i in range(0, 9, 3):
        if small_board[i] == small_board[i + 1] == player and small_board[i + 2] == 0:
            return i + 2
        elif small_board[i] == small_board[i + 2] == player and small_board[i + 1] == 0:
            return i + 1
        elif small_board[i + 1] == small_board[i + 2] == player and small_board[i] == 0:
            return i

    # Controleer op winnende kolommen
    for i in range(3):
        if small_board[i] == small_board[i + 3] == player and small_board[i + 6] == 0:
            return i + 6
        elif small_board[i] == small_board[i + 6] == player and small_board[i + 3] == 0:
            return i + 3
        elif small_board[i + 3] == small_board[i + 6] == player and small_board[i] == 0:
            return i

    # Controleer op winnende diagonalen
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

    # Geen winnende zet
    return None

def small_board_is_full(small_board):
    for x in small_board:
        if x == 0:
            return False
    else:
        return True


def small_board_evaluate(small_board):
    x3 = small_board_count(small_board, 1, 3)
    x2 = small_board_count(small_board, 1, 2)
    x1 = small_board_count(small_board, 1, 1)
    o3 = small_board_count(small_board, -1, 3)
    o2 = small_board_count(small_board, -1, 2)
    o1 = small_board_count(small_board, -1, 1)

    value = (10 * x3 + 3 * x2 + x1) - (10 * o3 + 3 * o2 + o1)
    return value


def small_board_count(small_board, player, n): #https://stackoverflow.com/questions/35357419/tic-tac-toe-rate-a-board-algorithm
    count = 0

    # Horizontale rijen
    for i in range(3):
        row = small_board[i * 3: (i + 1) * 3]
        if row.count(player) == n and row.count(0) == 3 - n:
            count += 1

    # Verticale rijen
    for i in range(3):
        column = [small_board[i], small_board[i + 3], small_board[i + 6]]
        if column.count(player) == n and column.count(0) == 3 - n:
            count += 1

    # Diagonalen
    diagonal1 = [small_board[0], small_board[4], small_board[8]]
    diagonal2 = [small_board[2], small_board[4], small_board[6]]
    if diagonal1.count(player) == n and diagonal1.count(0) == 3 - n:
        count += 1
    if diagonal2.count(player) == n and diagonal2.count(0) == 3 - n:
        count += 1

    return count



# Testcase 2: Bord met 2 X's in een rij
board2 = [1, 0, 1, 0, 1, 0, 0, 0, 0]
player2 = 1
value2 = small_board_evaluate(board2)
print(value2)  # Output: 16

# Testcase 3: Bord met 1 X in een rij
board3 = [0, 0, 0, 0, 0, 0, 1, 0, 0]
player3 = 1
value3 = small_board_evaluate(board3)
print(value3)  # Output: 1

# Testcase 4: Bord met 3 O's in een rij
board4 = [-1, 1, -1, -1, 1, -1, 1, -1, 0]
player4 = -1
value4 = small_board_evaluate(board4)
print(value4)  # Output: -27

# Testcase 5: Bord met 2 O's in een rij
board5 = [-1, 0, 0, 0, 1, 0, 0, 0, -1]
player5 = -1
value5 = small_board_evaluate(board5)
print(value5)  # Output: -16

# Testcase 6: Bord met 1 O in een rij
board6 = [1, 1, 0, 1, -1, 1, -1, 1, 0]
player6 = -1
value6 = small_board_evaluate(board6)
print(value6)  # Output: -1


def real_evaluate_square(small_board):
    evaluation = 0
    points = [0.2, 0.17, 0.2, 0.17, 0.22, 0.17, 0.2, 0.17, 0.2]

    for bw in range(len(small_board)):
        evaluation -= small_board[bw] * points[bw]

    a = 2
    if (
        small_board[0] + small_board[1] + small_board[2] == a
        or small_board[3] + small_board[4] + small_board[5] == a
        or small_board[6] + small_board[7] + small_board[8] == a
    ):
        evaluation -= 6
    if (
        small_board[0] + small_board[3] + small_board[6] == a
        or small_board[1] + small_board[4] + small_board[7] == a
        or small_board[2] + small_board[5] + small_board[8] == a
    ):
        evaluation -= 6
    if small_board[0] + small_board[4] + small_board[8] == a or small_board[2] + small_board[4] + small_board[6] == a:
        evaluation -= 7

    a = -1
    if (
        (small_board[0] + small_board[1] == 2 * a and small_board[2] == -a)
        or (small_board[1] + small_board[2] == 2 * a and small_board[0] == -a)
        or (small_board[0] + small_board[2] == 2 * a and small_board[1] == -a)
        or (small_board[3] + small_board[4] == 2 * a and small_board[5] == -a)
        or (small_board[3] + small_board[5] == 2 * a and small_board[4] == -a)
        or (small_board[5] + small_board[4] == 2 * a and small_board[3] == -a)
        or (small_board[6] + small_board[7] == 2 * a and small_board[8] == -a)
        or (small_board[6] + small_board[8] == 2 * a and small_board[7] == -a)
        or (small_board[7] + small_board[8] == 2 * a and small_board[6] == -a)
        or (small_board[0] + small_board[3] == 2 * a and small_board[6] == -a)
        or (small_board[0] + small_board[6] == 2 * a and small_board[3] == -a)
        or (small_board[3] + small_board[6] == 2 * a and small_board[0] == -a)
        or (small_board[1] + small_board[4] == 2 * a and small_board[7] == -a)
        or (small_board[1] + small_board[7] == 2 * a and small_board[4] == -a)
        or (small_board[4] + small_board[7] == 2 * a and small_board[1] == -a)
        or (small_board[2] + small_board[5] == 2 * a and small_board[8] == -a)
        or (small_board[2] + small_board[8] == 2 * a and small_board[5] == -a)
        or (small_board[5] + small_board[8] == 2 * a and small_board[2] == -a)
        or (small_board[0] + small_board[4] == 2 * a and small_board[8] == -a)
        or (small_board[0] + small_board[8] == 2 * a and small_board[4] == -a)
        or (small_board[4] + small_board[8] == 2 * a and small_board[0] == -a)
        or (small_board[2] + small_board[4] == 2 * a and small_board[6] == -a)
        or (small_board[2] + small_board[6] == 2 * a and small_board[4] == -a)
        or (small_board[4] + small_board[6] == 2 * a and small_board[2] == -a)
    ):
        evaluation -= 9

    a = -2
    if (
        small_board[0] + small_board[1] + small_board[2] == a
        or small_board[3] + small_board[4] + small_board[5] == a
        or small_board[6] + small_board[7] + small_board[8] == a
    ):
        evaluation += 6
    if (
        small_board[0] + small_board[3] + small_board[6] == a
        or small_board[1] + small_board[4] + small_board[7] == a
        or small_board[2] + small_board[5] + small_board[8] == a
    ):
        evaluation += 6
    if small_board[0] + small_board[4] + small_board[8] == a or small_board[2] + small_board[4] + small_board[6] == a:
        evaluation += 7

    a = 1
    if (
        (small_board[0] + small_board[1] == 2 * a and small_board[2] == -a)
        or (small_board[1] + small_board[2] == 2 * a and small_board[0] == -a)
        or (small_board[0] + small_board[2] == 2 * a and small_board[1] == -a)
        or (small_board[3] + small_board[4] == 2 * a and small_board[5] == -a)
        or (small_board[3] + small_board[5] == 2 * a and small_board[4] == -a)
        or (small_board[5] + small_board[4] == 2 * a and small_board[3] == -a)
        or (small_board[6] + small_board[7] == 2 * a and small_board[8] == -a)
        or (small_board[6] + small_board[8] == 2 * a and small_board[7] == -a)
        or (small_board[7] + small_board[8] == 2 * a and small_board[6] == -a)
        or (small_board[0] + small_board[3] == 2 * a and small_board[6] == -a)
        or (small_board[0] + small_board[6] == 2 * a and small_board[3] == -a)
        or (small_board[3] + small_board[6] == 2 * a and small_board[0] == -a)
        or (small_board[1] + small_board[4] == 2 * a and small_board[7] == -a)
        or (small_board[1] + small_board[7] == 2 * a and small_board[4] == -a)
        or (small_board[4] + small_board[7] == 2 * a and small_board[1] == -a)
        or (small_board[2] + small_board[5] == 2 * a and small_board[8] == -a)
        or (small_board[2] + small_board[8] == 2 * a and small_board[5] == -a)
        or (small_board[5] + small_board[8] == 2 * a and small_board[2] == -a)
        or (small_board[0] + small_board[4] == 2 * a and small_board[8] == -a)
        or (small_board[0] + small_board[8] == 2 * a and small_board[4] == -a)
        or (small_board[4] + small_board[8] == 2 * a and small_board[0] == -a)
        or (small_board[2] + small_board[4] == 2 * a and small_board[6] == -a)
        or (small_board[2] + small_board[6] == 2 * a and small_board[4] == -a)
        or (small_board[4] + small_board[6] == 2 * a and small_board[2] == -a)
    ):
        evaluation += 9

    evaluation -= small_board_check_winner(small_board) * 12

    return evaluation


# Testcase 1
pos1 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
print(real_evaluate_square(board2))
# Uitvoer: 0

# Testcase 2
pos2 = [1, -1, 0, 0, 1, 0, 0, 0, -1]
print(real_evaluate_square(board3))
# Uitvoer: -5

# Testcase 3
pos3 = [-1, -1, 1, 1, 0, 1, 0, -1, -1]
print(real_evaluate_square(board4))
# Uitvoer: -3

# Testcase 4
pos4 = [1, 1, 1, 0, 0, 0, -1, -1, 0]
print(real_evaluate_square(board5))
# Uitvoer: 1

# Testcase 5
pos5 = [-1, 1, 0, 0, -1, 0, 0, 1, 1]
print(real_evaluate_square(board6))
# Uitvoer: -2