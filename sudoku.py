# Import the pygame, math and random packages
import pygame
import math
import random
# initialize the window
pygame.init()
# Create a screen
screen = pygame.display.set_mode((1200, 900))
# Name the window "Sudoku"
pygame.display.set_caption("Sudoku")
# Set up a clock
clock = pygame.time.Clock()

# Set up variables
# Make a variable that will allow the user to close the window
running = True
# Make variables for background colors
background_color = (255, 255, 255)
bkgd_dark = (192, 192, 192)
inst_bkgd = (198, 226, 255)
# Variables for the other colors
black = (0, 0, 0)
green = (50, 200, 50)
red = (200, 50, 50)
blue = (127, 255, 212)
dark_blue = (0, 0, 180)
# Make fonts
myfont = pygame.font.SysFont(None, 34)
arial_font = pygame.font.SysFont('arial', 34)
# Create an empty string for the user to input numbers
number = ""

# variables for drawing the grid
top = 50
bottom = 850
left = 50
right = 850
num_lines = 9
diff_vertical = math.ceil((right-left) / num_lines)
diff_horizontal = math.ceil((bottom - top) / num_lines)
buttonsX = right + 80
button_width = 150
button_width_2 = 220
button_height = 50
button_top = top + 200
easyX = 500
easyY = 400
hardX = 500
hardY = 500
global row, column
row = 0
column = 0
# make a variable for if the instruction screen should show
select_level = True


# function to display the instruction screen
def instruction_screen(select_level):
    # Make the background blue
    screen.fill(inst_bkgd)
    # Print the instructions
    inst = arial_font.render('How to play:', True, black)
    screen.blit(inst, (500, 100))
    inst = arial_font.render('Click on a box and type a number to enter a guess.', True, black)
    screen.blit(inst, (250, 150))
    inst = arial_font.render('Click the undo button to delete the last try.', True, black)
    screen.blit(inst, (250, 200))
    inst = arial_font.render('Please select difficulty level, then wait while the game board generates.', True, black)
    screen.blit(inst, (250, 250))
    # Draw the buttons for the difficulty levels
    # easy level
    pygame.draw.rect(screen, green, (easyX, easyY, button_width, button_height))
    easy = arial_font.render("Easy", True, black)
    screen.blit(easy, (easyX+40, easyY+5))
    # hard level
    pygame.draw.rect(screen, red, (hardX, hardY, button_width, button_height))
    hard = arial_font.render("Hard", True, black)
    screen.blit(hard, (hardX+40, hardY+5))
    # update the screen
    pygame.display.update()
    # check for input while the user hasn't selected a difficulty level
    while select_level:
        difficulty = 0
        # Set up a clock
        clock.tick(40)
        # Check for user input
        for event in pygame.event.get():
            # If the user hits the close button
            if event.type == pygame.QUIT:
                # Change the variable to false, which will exit the loop.
                select_level = False
            # If the user clicks the mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the coordinates of the mouse
                (mouseX, mouseY) = pygame.mouse.get_pos()
                # check if the user clicked on the easy level or hard level
                if easyX < mouseX < button_width+easyX:
                    if easyY < mouseY < button_height + easyY:
                        select_level = False
                        # print 40 random starting numbers if the user selected the easy level
                        difficulty = 40
                    if hardY < mouseY < button_height + hardY:
                        select_level = False
                        # print 20 random starting numbers if the user selected the hard level
                        difficulty = 20
    # return the difficulty level
    return difficulty


# display the instruction screen and store the user's choice of difficulty level
difficulty = instruction_screen(select_level)


# Define a function that checks if a number is already present in the row, column, or 3 by 3 subgrid
def safe(pos, num, grid):
    # check if the number is in the row
    row = pos[0]
    for i in range(9):
        if num == grid[row][i]:
            return False
    # check if the number is in the column
    col = pos[1]
    for i in range(9):
        if num == grid[i][col]:
            return False
    # check if the number is in the subgrid
    grid_r = row // 3 * 3
    grid_c = col // 3 * 3
    for i in range(grid_r, grid_r + 3):
        for j in range(grid_c, grid_c + 3):
            if grid[i][j] == num:
                return False
    # return true if the position is safe
    return True


# Define a function to find an empty location in the grid
def find_empty(arr):
    # loop over the rows
    for i in range(9):
        # loop over the columns
        for j in range(9):
            # return True and the position if the entry is 0
            if arr[i][j] == 0:
                return True, [i, j]
    # return False and False for the position if there are no empty positions
    return False, False


# Define a function that generates a random starting board
def rand_board():
    # counting variable
    num = 0
    # create an "empty" array of 0's
    arr = [[0 for i in range(9)] for j in range(9)]
    # create 27 random entries. The minimum number of entries for a unique solution
    # board is 17, so create more than the necessary 17 entries
    while num < 27:
        # get a random integer from 1-9
        rand = random.randint(1, 9)
        # get a random position in the array
        pos = [random.randint(0, 8), random.randint(0, 8)]
        # if the random position already has an entry, keep trying other random
        # positions until you find an empty one
        while arr[pos[0]][pos[1]] != 0:
            pos = [random.randint(0, 8), random.randint(0, 8)]
        # assign the random number to the random position if it is safe to do so
        if safe(pos, rand, arr):
            arr[pos[0]][pos[1]] = rand
            # increment the counter
            num += 1
    # return the array
    return arr


# Define a backtracking function to create a solution grid given a partially filled in grid
def find_solution(arr):
    # store whether or not the array is empty and the position of the next empty space
    empty, pos = find_empty(arr)
    # base case: the grid is filled, so return true
    if not empty:
        return True
    # store the row and column of the empty position
    row = pos[0]
    col = pos[1]
    # loop over the integers 1-9
    for num in range(1, 10):
        # assign the number to the current position if it is safe to do so
        if safe(pos, num, arr):
            arr[row][col] = num
            # recursively check if this leads to a solution
            if find_solution(arr):
                return True
            # if the number did not lead to a solution, empty the current position to try again
            arr[row][col] = 0
    # return False if none of the numbers are safe to add
    return False


# Define a function to create a filled in grid for the current game
def make_grid():
    # start with no solution
    sol = False
    # loop until a solution is found
    while not sol:
        # start with a random, partially filled in board
        arr = rand_board()
        # check to see if the board has a solution
        sol = find_solution(arr)
    # return the game board
    return arr


# Get a random solved grid
grid = make_grid()


# Define a function that will print the starting board on the screen
def draw_board(arr, difficulty):
    i = 0
    # fill in as many numbers as the difficulty setting
    while i <= difficulty:
        # get a random position
        pos = [random.randint(0, 8), random.randint(0, 8)]
        # store the value at that position
        x = str(arr[pos[0]][pos[1]])
        # check that the random position has not already been filled in
        if x != '0':
            # increase the counter
            i += 1
            # print the entry to the screen
            num = myfont.render(x, True, dark_blue)
            screen.blit(num, (left + (pos[0] * diff_vertical) + (diff_vertical / 2) - 5,
                              top + (pos[1] * diff_horizontal) + (diff_horizontal / 2) - 5))
            # delete the entry at that position so we know which positions have been used already
            arr[pos[0]][pos[1]] = 0
    # return the new grid with the entries that are printed on the screen deleted
    return arr


# Define a function that sets up the screen
def draw_screen(grid, difficulty):
    # Make the background white
    screen.fill(background_color)
    # Shade the 3 by 3 smaller sub grids a darker background color
    pygame.draw.rect(screen, bkgd_dark, (left, top, 3 * diff_vertical, 3 * diff_horizontal))
    pygame.draw.rect(screen, bkgd_dark, (left + (3 * diff_horizontal), top + (3 * diff_vertical),
                                         3 * diff_vertical, 3 * diff_horizontal))
    pygame.draw.rect(screen, bkgd_dark, (left + (6 * diff_horizontal), top, 3 * diff_vertical,
                                         3 * diff_horizontal))
    pygame.draw.rect(screen, bkgd_dark, (left, top + (6 * diff_vertical), 3 * diff_vertical,
                                         3 * diff_horizontal))
    pygame.draw.rect(screen, bkgd_dark, (left + (6 * diff_horizontal), top + (6 * diff_vertical),
                                         3 * diff_vertical, 3 * diff_horizontal))
    # Draw the 9 by 9 grid
    # Draw the vertical lines
    for i in range(10):
        vertical = left + (diff_vertical * i)
        pygame.draw.line(screen, black, (vertical, bottom), (vertical, top), 2)
    # Draw the horizontal lines
    for x in range(10):
        horizontal = top + (diff_horizontal * x)
        pygame.draw.line(screen, black, (left, horizontal), (right, horizontal), 2)
    # make the undo button
    pygame.draw.rect(screen, blue, (buttonsX, button_top, button_width_2, button_height + 10))
    undo = arial_font.render("Undo Last Move", True, black)
    screen.blit(undo, (buttonsX + 5, button_top + 10))
    # Fill in the starting grid
    arr = draw_board(grid, difficulty)
    # Display the screen
    pygame.display.update()
    return arr


# Run the function that sets up the screen and store the new array
arr = draw_screen(grid, difficulty)


# Function to return which box the mouse clicked on
def click_box(mouseX, mouseY):
    # Check if the mouse is inside the grid
    if left < mouseX < right and top < mouseY < bottom:
        # check which row the mouse is in
        for i in range(num_lines):
            if left + (diff_vertical * i) < mouseX < left + (diff_vertical * (i + 1)):
                row = i
        # check which column the mouse is in
        for i in range(num_lines):
            if top + (diff_vertical * i) < mouseY < top + (diff_vertical * (i + 1)):
                column = i
        return row, column
    # if the mouse is not in the grid, return false
    return False, False


# Create a loop that continues until the user hits the close button
while running:
    # Set up a clock
    clock.tick(40)
    # Check for user input
    for event in pygame.event.get():
        # check if the user hits the close button
        if event.type == pygame.QUIT:
            # Change the running variable to false, which will exit the loop.
            running = False
        # check if the user clicks the mouse
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the coordinates of the mouse
            (mouseX, mouseY) = pygame.mouse.get_pos()
            # Check if the user clicked on the undo button
            if buttonsX < mouseX < buttonsX + button_width_2 \
                    and button_top < mouseY < button_top + button_height + 10:
                # make sure the user has clicked on a square (row isn't False)
                if type(row) == int:
                    # check that the user is not trying to delete a hint entry
                    if arr[row][column] != 0:
                        # check if the background is grey
                        if 0 <= row <= 2 or 6 <= row <= 8:
                            if 0 <= column <= 2 or 6 <= column <= 8:
                                # Delete the current row and column entry by drawing a grey square
                                pygame.draw.rect(screen, bkgd_dark, (left + (row * diff_vertical) + 5,
                                                                     top + (column * diff_horizontal) + 5,
                                                                     diff_vertical - 10, diff_horizontal - 10))
                                # update the screen
                                pygame.display.update()
                            else:
                                # Delete the current row and column entry by drawing a white square
                                pygame.draw.rect(screen, background_color,
                                                 (left + (row * diff_vertical) + 5,
                                                  top + (column * diff_horizontal) + 5, diff_vertical - 10,
                                                  diff_horizontal - 10))
                                # update the screen
                                pygame.display.update()
                        elif 3 <= column <= 5:
                            # Delete the current row and column entry by drawing a grey square
                            pygame.draw.rect(screen, bkgd_dark, (left + (row * diff_vertical) + 5,
                                                                 top + (column * diff_horizontal) + 5,
                                                                 diff_vertical - 10, diff_horizontal - 10))
                            pygame.display.update()
                        else:
                            # Delete the current row and column entry by drawing a white square
                            pygame.draw.rect(screen, background_color, (left + (row * diff_vertical) + 5,
                                                                        top + (column * diff_horizontal) + 5,
                                                                        diff_vertical - 10, diff_horizontal - 10))
                            pygame.display.update()
            else:
                # If the user has not clicked on the undo button, run the function that returns
                # the row and column of the box the user clicked on
                row, column = click_box(mouseX, mouseY)
        # check for text input from the user
        elif event.type == pygame.TEXTINPUT:
            # check that the user has selected a box (row isn't False)
            if type(row) == int:
                # concatenate what the user types onto the end of the message
                number += event.text
                # check that the user didn't try to change one of the starting hint numbers
                if arr[row][column] != 0:
                    # Turn the message into an image and put the image on the screen
                    msg = myfont.render(number, True, black)
                    screen.blit(msg, (left + (row * diff_vertical) + (diff_vertical / 2) - 5,
                                      top + (column * diff_horizontal) + (diff_horizontal / 2) - 5))
                    # check if the guess was correct
                    if int(number) != arr[row][column]:
                        # if the guess was incorrect, display a red outline
                        pygame.draw.rect(screen, red, (left + (row * diff_vertical) + 10,
                                                       top + (column * diff_horizontal) + 10,
                                                       diff_vertical - 20, diff_horizontal - 20), width=5)
                    # reset the message to print back to blank
                    number = ''
                    # update the screen
                    pygame.display.update()


# Stop running the program
pygame.quit()
