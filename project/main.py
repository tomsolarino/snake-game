import os
import keyboard  # using module keyboard
import time

# Global Variables
snake_head_loc = [0, 0]
snake_head_dir = [1, 0]
cols, rows = (50, 10)
playground = [[" " for i in range(cols)] for j in range(rows)]


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


# Draw the border around the map
def DrawPlaygroundBorder(playground):
    for row in range(rows):
        playground[row][0] = "║"
        playground[row][cols - 1] = "║"

    for col in range(cols):
        playground[0][col] = "═"
        playground[rows - 1][col] = "═"

    # Set border corners
    playground[0][0] = "╔"
    playground[0][cols - 1] = "╗"
    playground[rows - 1][0] = "╚"
    playground[rows - 1][cols - 1] = "╝"


# This function will draw the main menu
def draw_main_menu(playground):
    os.system('cls')

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
    playground[snake_head_loc[0]][snake_head_loc[1]] = '@'


# Draws the game after it was updated
def draw_game(playground):
    os.system('cls')
    screen = ''
    for row in range(rows):
        for col in range(cols):
            screen = screen + playground[row][col]
        screen = screen + '\n'
    print(screen)


# Gets the players decision to play or not
def should_play():
    while(True):
        if keyboard.read_key() == "y":
            return True
        if keyboard.read_key() == "q":
            return False


# The main gameplay loop
def main_gameplay_loop():
    draw_main_menu(playground)

    if should_play():
        playing = True
        ClearPlayground()
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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_gameplay_loop()
