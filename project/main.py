import os
import time
import random

if os.name == 'nt':
    import keyboard  # using module keyboard "pip install keyboard"
elif os.name == 'posix':
    from pynput import keyboard


# Global Variables
playing = False
snake_body_parts = [[0, 0]]
snake_head_dir = [1, 0]  # The snakes current direction of motion
snake_food_loc = [1, 0]  # The grid location of the snakes next food piece
cols, rows = (20, 10)  # The size of the map / playground
playground = [[" " for i in range(cols)] for j in range(rows)]  # The playground 2d array
last_key_pressed = ""  # The last key pressed on the keyboard


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


# Clears the terminal for mac or windows os
def ClearScreen():
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')


# Called if the player collides with themself or the edge of the map
def game_over():
    ClearScreen()
    ClearPlayground()
    global snake_body_parts

    center_text(playground, 2, "GAME OVER!")
    center_text(playground, 3, "SCORE " + str(len(snake_body_parts)))
    center_text(playground, 6, "PRESS Y TO BEGIN")
    center_text(playground, 7, "Q TO QUIT")

    screen = ''
    for row in range(rows):
        for col in range(cols):
            screen = screen + playground[row][col]
        screen = screen + '\n'
    print(screen)

    if (should_play()):
        snake_body_parts = [[0, 0]]
        # Center the snake's head in the map
        snake_body_parts[0][0] = round(rows / 2)  # row
        snake_body_parts[0][1] = round(cols / 2)  # col
        # Randomize the first piece of food
        new_food_position()
    else:
        global playing
        playing = False


# checks if the game should end
def check_game_over():
    # Check that the snakes head didn't hit the edge of the map
    if snake_body_parts[0][0] > rows - 2 or snake_body_parts[0][0] < 1 or snake_body_parts[0][1] > cols - 2 or snake_body_parts[0][1] < 1:
        game_over()
        return
    # Check that the snake didn't collide with itself
    for elem in snake_body_parts:
        if snake_body_parts.count(elem) > 1:
            game_over()
            return


# Updates the game
def update_game(playground):
    if (snake_body_parts[0][0] + snake_head_dir[0] == snake_food_loc[0]) and (snake_body_parts[0][1] + snake_head_dir[1] == snake_food_loc[1]):
        new_food_position()
        snake_body_parts.append([0, 0])

    # Move all the body parts of the snake forward
    for i in range(len(snake_body_parts)-1, -1, -1):
        if i == 0:
            snake_body_parts[i][0] += snake_head_dir[0]
            snake_body_parts[i][1] += snake_head_dir[1]
        else:
            snake_body_parts[i][0] = snake_body_parts[i - 1][0]
            snake_body_parts[i][1] = snake_body_parts[i - 1][1]

    check_game_over()


# Draws the game after it was updated
def draw_game(playground):
    # Clear the background and terminal before drawing the snake
    ClearScreen()
    ClearPlayground()

    # Draw the snakes head / body
    for part in snake_body_parts:
        playground[part[0]][part[1]] = 'O'
    playground[snake_body_parts[0][0]][snake_body_parts[0][1]] = '@'

    # Draw the snakes food location
    playground[snake_food_loc[0]][snake_food_loc[1]] = '¤'

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
        global last_key_pressed
        if last_key_pressed in [121, 89, "y", "Y"]:  # (Y / y)
            last_key_pressed = ''
            return True
        if last_key_pressed in [113, 81, "q", "Q", "esc"]:  # (Q / q / escape)
            return False


# Create a new random position for the snakes food
# Make sure that is ins't on the snake though!
def new_food_position():
    new_loc = [random.randint(1, rows - 2), random.randint(1, cols - 2)]

    # if the food is going to appear where the snakes head is about to go
    if (snake_food_loc == new_loc):
        new_food_position()
        return

    # If the food is about to appear where another part of the snake exists
    for part in snake_body_parts:
        if part == new_loc:
            new_food_position()
            return

    # Fianlly if all tests past set the new foods position
    snake_food_loc[0] = new_loc[0]
    snake_food_loc[1] = new_loc[1]


# Called when a key is pressed
def on_press(key):
    global last_key_pressed
    global snake_head_dir
    try:
        last_key_pressed = key.char
    except AttributeError:
        last_key_pressed = key.name

    # Change the snakes direction of motion based off user input
    # Make sure the snake cannot go back on its self
    if last_key_pressed in ["left", "a", "A"] and snake_head_dir[1] != 1:
        snake_head_dir = [0, -1]
    elif last_key_pressed in ["right", "d", "D"] and snake_head_dir[1] != -1:
        snake_head_dir = [0, 1]
    elif last_key_pressed in ["up", "w", "W"] and snake_head_dir[0] != 1:
        snake_head_dir = [-1, 0]
    elif last_key_pressed in ["down", "s", "S"] and snake_head_dir[0] != -1:
        snake_head_dir = [1, 0]


# The main gameplay loop
def main_gameplay_loop():
    # Start by drawing the main menu
    draw_main_menu(playground)

    # Checks if the user want to play or not
    if should_play():
        global playing
        playing = True
        next_update = 0

        # Center the snake's head in the map
        snake_body_parts[0][0] = round(rows / 2)  # row
        snake_body_parts[0][1] = round(cols / 2)  # col

        # Randomize the first piece of food
        new_food_position()

        # Game Update Loop (every one second update)
        while (playing):
            if (time.time() > next_update):
                next_update = time.time() + 0.75
                update_game(playground)
                draw_game(playground)

    ClearScreen()


# This is the entry point for the main script
if __name__ == '__main__':
    # Collect keyboard events in a non-blocking fashion:
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Run the main gameplay loop
    main_gameplay_loop()

    # Finally stop the keyboard listner
    listener.stop()
