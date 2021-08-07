import os
import time

if os.name == 'nt':
    import keyboard  # using module keyboard "pip install keyboard"
elif os.name == 'posix':
    import sys
    import tty
    from pynput import keyboard


# Global Variables
snake_head_loc = [0, 0]
snake_head_dir = [1, 0]
cols, rows = (50, 10)
playground = [[" " for i in range(cols)] for j in range(rows)]
last_key_pressed = ""


# This function will center a string on a certain line in the window
def center_text(arr, target_row, text):
    text_start_pos = round((cols - 2 - text.__len__()) / 2)

    for c in range(text.__len__()):
        arr[target_row][text_start_pos + c] = text[c]


# Completely clear the map
def ClearPlayground():
    for row in range(rows):
        for col in range(cols):
            # Set border edges
            if (row == 0 or row == rows - 1):
                playground[row][col] = "═"
            elif (col == 0 or col == cols - 1):
                playground[row][col] = "║"
            else:
                playground[row][col] = " "

    # Set border corners
    playground[0][0] = "╔"
    playground[0][cols - 1] = "╗"
    playground[rows - 1][0] = "╚"
    playground[rows - 1][cols - 1] = "╝"


# This function will draw the main menu
def draw_main_menu(playground):
    ClearScreen()
    ClearPlayground()

    center_text(playground, 2, "SNAKE GAME")
    center_text(playground, 3, "BY TOM")
    center_text(playground, 6, "PRESS Y TO BEGIN")
    center_text(playground, 7, "Q TO QUIT")

    screen = ''
    for row in range(rows):
        for col in range(cols):
            screen = screen + playground[row][col]
        screen = screen + '\n'
    print(screen)


# Updates the game
def update_game(playground):
    # TODO: Update snakes head loc
    # The snake itself might be a list of locations (row / col) i.e. head is index 0 at pos 5, 8
    snake_head_loc[0] += snake_head_dir[0]
    snake_head_loc[1] += snake_head_dir[1]


# Clears the terminal for mac or windows os
def ClearScreen():
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')


# Draws the game after it was updated
def draw_game(playground):
    # Clear the background and terminal before drawing the snake
    ClearScreen()
    ClearPlayground()

    # Draw the snakes head / body
    playground[snake_head_loc[0]][snake_head_loc[1]] = '@'

    screen = ''
    for row in range(rows):
        for col in range(cols):
            screen = screen + playground[row][col]
        screen = screen + '\n'
    print(screen)


# Gets the players decision to play or not
# Will wait until either 'y' or 'q' is clicked
def should_play():
    while(True):
        if last_key_pressed in [121, 89, "y", "Y"]:  # (Y / y)
            return True
        if last_key_pressed in [113, 81, "q", "Q", "esc"]:  # (Q / q)
            return False


# Called when a key is pressed
def on_press(key):
    global last_key_pressed
    global snake_head_dir
    try:
        last_key_pressed = key.char
    except AttributeError:
        last_key_pressed = key.name

    if last_key_pressed in ["left", ""]:
        snake_head_dir = [0, -1]
    elif last_key_pressed in ["right", ""]:
        snake_head_dir = [0, 1]
    elif last_key_pressed in ["up", ""]:
        snake_head_dir = [-1, 0]
    elif last_key_pressed in ["down", ""]:
        snake_head_dir = [1, 0]

    print(last_key_pressed)


# Called when a key is released
def on_release(key):
    pass
    # print('{0} released'.format(
    #     key))
    # if key == keyboard.Key.esc:
    #     # Stop listener
    #     return False


# The main gameplay loop
def main_gameplay_loop():
    # For input on mac
    if os.name == 'posix':
        tty.setcbreak(sys.stdin)

    # Start by drawing the main menu
    draw_main_menu(playground)

    # Checks if the user want to play or not
    if should_play():
        playing = True
        next_update = 0

        # Center the snake's head in the map
        snake_head_loc[0] = round(rows / 2)  # row
        snake_head_loc[1] = round(cols / 2)  # col

        # Game Update Loop (every one second update)
        while (playing):
            if (time.time() > next_update):
                next_update = time.time() + 1
                update_game(playground)
                draw_game(playground)


# This is the entry point for the main script
if __name__ == '__main__':
    # Collect keyboard events in a non-blocking fashion:
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    # Run the main gameplay loop
    main_gameplay_loop()

    # Finally stop the keyboard listner
    listener.stop()
