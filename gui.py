import tkinter as tk
from ai import small_board_check, minimax
from game_state import board, board_status
import tkinter.messagebox as messagebox

current_player = "X"  # Startspeler
active_frames = []  # Huidig actieve frame
current_board = 0


def check_game_winner():
    winning_combinations = [
        # Horizontale combinaties
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        # Verticale combinaties
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        # Diagonale combinaties
        [0, 4, 8], [2, 4, 6]
    ]

    for combination in winning_combinations:
        indices = combination
        marks = [board_status[i] for i in indices]
        if all(mark == marks[0] and mark != 0 for mark in marks):
            winner = marks[0]
            if winner == 1:
                messagebox.showinfo("Game Over", "Speler X wint het spel!")
            else:
                messagebox.showinfo("Game Over", "Speler O wint het spel!")
            game_board.after(5000, game_board.destroy)  # Sluit de GUI na 5 seconden
            return

    if all(status != 0 for status in board_status):
        messagebox.showinfo("Game Over", "Gelijkspel!")
        game_board.after(5000, game_board.destroy)  # Sluit de GUI na 5 seconden


def change_button_text(frame_index, button_index):
    global current_player, active_frames, current_board

    if buttons[frame_index][button_index]["text"] == "" and board_status[frame_index] != -1:
        buttons[frame_index][button_index].configure(text=current_player)
        game_board.update()  # Bijwerken van de GUI om de zet weer te geven
        game_board.after(100)  # Voeg een kleine vertraging toe voor een soepelere weergave

        if current_player == "X":
            current_player = "O"
            board[frame_index][button_index] = -1  # Toevoegen van -1 voor speler X
            current_board = button_index  # Bijwerken van de huidige locatie naar het gekozen vakje
            perform_computer_move()  # Na zet van X, voert de computer een zet uit
        else:
            current_player = "X"
            board[frame_index][button_index] = 1  # Toevoegen van 1 voor speler O
        small_board_check(buttons, frame_index)

    active_frames = []  # Lijst om bij te houden welke frames groen moeten zijn

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
            frame.configure(bg="light green")
        else:
            frame = frames[x]
            small_board_disable_buttons(x)
            frame.configure(bg="black")
    print(board_status)
    print(board)

    game_board.after(100)  # Voeg een kleine vertraging toe voordat de winnaar wordt gecontroleerd
    check_game_winner()  # Controleer of het hele spel is gewonnen

    active_frames.clear()


def perform_computer_move():
    global current_player, current_board

    if current_player == "O":
        frame_index, button_index = computer_move()
        if frame_index is not None and button_index is not None:
            game_board.after(100)  # Voeg een kleine vertraging toe voor een soepelere weergave
            change_button_text(frame_index, button_index)
            current_board = button_index  # Bijwerken van de huidige locatie naar het gekozen vakje


def computer_move():
    if board_status[current_board] == -1:
        _, best_play = minimax(board, current_board, 5, float("-inf"), float("inf"), True)
        if best_play is not None:
            frame_index, button_index = best_play
            return frame_index, button_index
    else:
        _, best_play = minimax(board, current_board, 5, float("-inf"), float("inf"), True)
        if best_play is not None:
            button_index = best_play[1]
            return current_board, button_index
    return None, None

def small_board_disable_buttons(frame_index):
    buttons_in_frame = buttons[frame_index]
    for x in buttons_in_frame:
        x.config(state="disabled")


def small_board_enable_buttons(frame_index):
    buttons_in_frame = buttons[frame_index]
    for x in buttons_in_frame:
        x.config(state="normal")


game_board = tk.Tk()
game_board.title("Ultimate Tic Tac Toe")

frames = []
buttons = []

# Frames voor het speelveld
for frame_index in range(9):
    frame = tk.Frame(game_board, width=312, height=312, bg="light green", bd=4)
    frame.grid(row=frame_index // 3, column=frame_index % 3, padx=2, pady=2)
    frames.append(frame)

# Knoppen in elk frame
for frame_index in range(9):
    button_frame = frames[frame_index]
    button_list = []
    for button_index in range(9):
        button = tk.Button(button_frame, width=8, height=3, bg="white", bd=2,
                           command=lambda frame=frame_index, btn=button_index: change_button_text(frame, btn))
        button.grid(row=button_index // 3, column=button_index % 3, padx=2, pady=2)
        button_list.append(button)
    buttons.append(button_list)


game_board.mainloop()

print(buttons)
print(frames)
