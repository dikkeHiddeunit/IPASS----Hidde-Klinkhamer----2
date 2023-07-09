import tkinter as tk
from ai import small_board_check
from game_state import board, board_status

current_player = "X"  # Startspeler
active_frames = []  # Huidig actieve frame


def change_button_text(frame_index, button_index):
    global current_player, active_frame

    if buttons[frame_index][button_index]["text"] == "" and board_status[frame_index] != -1:
        buttons[frame_index][button_index].configure(text=current_player)
        if current_player == "X":
            current_player = "O"
            board[frame_index][button_index] = -1  # Toevoegen van -1 voor speler X
        else:
            current_player = "X"
            board[frame_index][button_index] = 1  # Toevoegen van 1 voor speler O
        small_board_check(frame_index)

    active_frames = []  # Lijst om bij te houden welke frames groen moeten zijn

    if board_status[button_index] == 0:
        active_frames.append(button_index)
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
    active_frames.clear()

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
        button = tk.Button(button_frame, width=8, height=3, bg="white", bd=2, command=lambda frame=frame_index, btn=button_index: change_button_text(frame, btn))
        button.grid(row=button_index // 3, column=button_index % 3, padx=2, pady=2)
        button_list.append(button)
    buttons.append(button_list)

game_board.mainloop()


print(buttons)
print(frames)
