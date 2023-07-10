import tkinter as tk
from ai import small_board_check, minimax
from game_state import board, board_status, frame_winner
import tkinter.messagebox as messagebox

current_player = "X"  # Starting player
active_frames = []  # Currently active frames
current_board = 0

difficulty = input("Choose a difficulty level: easy/hard --> ")
if difficulty == "easy":
    difficulty = 1
elif difficulty == "hard":
    difficulty = 5
else:
    print("ERROR")
    exit()

def check_game_winner():
    # Checks if there is a winner in the game
    game_winner = False
    winner = 0

    # Check rows
    if frame_winner[0] == frame_winner[1] == frame_winner[2] and frame_winner[0] != 0:
        winner = frame_winner[0]
        game_winner = True
    elif frame_winner[3] == frame_winner[4] == frame_winner[5] and frame_winner[3] != 0:
        winner = frame_winner[3]
        game_winner = True
    elif frame_winner[6] == frame_winner[7] == frame_winner[8] and frame_winner[6] != 0:
        winner = frame_winner[6]
        game_winner = True

    # Check columns
    elif frame_winner[0] == frame_winner[3] == frame_winner[6] and frame_winner[0] != 0:
        winner = frame_winner[0]
        game_winner = True
    elif frame_winner[1] == frame_winner[4] == frame_winner[7] and frame_winner[1] != 0:
        winner = frame_winner[1]
        game_winner = True
    elif frame_winner[2] == frame_winner[5] == frame_winner[8] and frame_winner[2] != 0:
        winner = frame_winner[2]
        game_winner = True

    # Check diagonals
    elif frame_winner[0] == frame_winner[4] == frame_winner[8] and frame_winner[0] != 0:
        winner = frame_winner[0]
        game_winner = True
    elif frame_winner[2] == frame_winner[4] == frame_winner[6] and frame_winner[2] != 0:
        winner = frame_winner[2]
        game_winner = True

    if game_winner == True and winner == 1:
        messagebox.showinfo("Game Over", "Player X wins the game! The window will close automatically.")
        game_board.after(5000, game_board.destroy)  # Close the GUI after 5 seconds
    elif game_winner == True and winner == -1:
        messagebox.showinfo("Game Over", "Player O wins the game! The window will close automatically.")
        game_board.after(5000, game_board.destroy)  # Close the GUI after 5 seconds
    else:
        if all(status != 0 for status in board_status):
            messagebox.showinfo("Game Over", "It's a draw! The window will close automatically.")
            game_board.after(5000, game_board.destroy)  # Close the GUI after 5 seconds
    return

def change_button_text(frame_index, button_index):
    # Changes the text and updates the button state when a button is clicked
    global current_player, active_frames, current_board
    if buttons[frame_index][button_index]["text"] == "" and board_status[frame_index] != -1:
        buttons[frame_index][button_index].configure(text=current_player)
        if current_player == "X":
            buttons[frame_index][button_index].configure(bg="tomato")  # Color for player X
        else:
            buttons[frame_index][button_index].configure(bg="cornflowerblue")  # Color for player O
        game_board.update()  # Update the GUI to display the move
        game_board.after(100)  # Add a small delay for smoother display

        if current_player == "X":
            current_player = "O"
            board[frame_index][button_index] = -1  # Add -1 for player X's move
            small_board_check(buttons, frame_index)
            current_board = button_index  # Update the current board location to the chosen button
            perform_computer_move()  # After X's move, the computer makes a move
        else:
            current_player = "X"
            board[frame_index][button_index] = 1  # Add 1 for player O's move
            small_board_check(buttons, frame_index)
        small_board_check(buttons, frame_index)

    active_frames = []  # List to keep track of frames that should be highlighted

    if board_status[current_board] == 0:
        active_frames.append(current_board)
    else:
        for x in range(9):
            if board_status[x] == 0:
                active_frames.append(x)

    for x in range(9):
        if x in active_frames:
            frame = frames[x]
            small_board_enable_buttons(x)
            frame.configure(bg="green")
        else:
            frame = frames[x]
            small_board_disable_buttons(x)
            frame.configure(bg="black")

    game_board.after(100)  # Add a small delay before checking for the winner
    check_game_winner()  # Check if the entire game has been won

    active_frames.clear()

def perform_computer_move():
    # Performs the computer's move
    global current_player, current_board

    if current_player == "O":
        frame_index, button_index = computer_move()
        if frame_index is not None and button_index is not None:
            game_board.after(100)  # Add a small delay for smoother display
            change_button_text(frame_index, button_index)
            current_board = button_index  # Update the current board location to the chosen button

def computer_move():
    # Determines the computer's move
    if board_status[current_board] == -1:
        _, best_play = minimax(board, current_board, difficulty, float("-inf"), float("inf"), True)
        if best_play is not None:
            frame_index, button_index = best_play
            return frame_index, button_index
    else:
        _, best_play = minimax(board, current_board, difficulty, float("-inf"), float("inf"), True)
        if best_play is not None:
            button_index = best_play[1]
            return current_board, button_index
    return None, None

def small_board_disable_buttons(frame_index):
    # Disables the buttons in a small board frame
    buttons_in_frame = buttons[frame_index]
    for x in buttons_in_frame:
        x.config(state="disabled")

def small_board_enable_buttons(frame_index):
    # Enables the buttons in a small board frame
    buttons_in_frame = buttons[frame_index]
    for x in buttons_in_frame:
        x.config(state="normal")

game_board = tk.Tk()
game_board.title("Ultimate Tic Tac Toe")

frames = []
buttons = []

# Frames for the game board
for frame_index in range(9):
    frame = tk.Frame(game_board, width=312, height=312, bg="green", bd=4)
    frame.grid(row=frame_index // 3, column=frame_index % 3, padx=2, pady=2)
    frames.append(frame)

# Buttonsin each frame
for frame_index in range(9):
    button_frame = frames[frame_index]
    button_list = []
    for button_index in range(9):
        button = tk.Button(button_frame, width=8, height=3, bg="white", bd=2, command=lambda frame=frame_index, btn=button_index: change_button_text(frame, btn))
        button.grid(row=button_index // 3, column=button_index % 3, padx=2, pady=2)
        button_list.append(button)
    buttons.append(button_list)

game_board.mainloop()

