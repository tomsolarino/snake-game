import os


# This function will center a string on a certain line in the window
def center_text(arr, target_row, text):
    # rows = arr.__len__()
    cols = arr[0].__len__()

    text_start_pos = round((cols - 2 - text.__len__()) / 2)

    for c in range(text.__len__()):
        arr[target_row][text_start_pos + c] = text[c]


# This function will draw the main menu
def draw_main_menu():
    os.system('cls')
    cols, rows = (50, 10)
    arr = [[" " for i in range(cols)] for j in range(rows)]

    center_text(arr, 2, "SNAKE GAME")
    center_text(arr, 3, "BY TOM")
    center_text(arr, 6, "PRESS Y TO BEGIN")

    for row in range(rows):
        for col in range(cols):
            # Set border edges
            if (row == 0 or row == rows - 1):
                arr[row][col] = "═"
            if (col == 0 or col == cols - 1):
                arr[row][col] = "║"

            # Set border corners
            arr[0][0] = "╔"
            arr[0][cols - 1] = "╗"
            arr[rows - 1][0] = "╚"
            arr[rows - 1][cols - 1] = "╝"

            # Finally draw the final screen
            print(arr[row][col], end="", flush=True)

        print("")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    playing = True

    while (playing):
        draw_main_menu()
        name = input('What is your name? ')
        playing = False
