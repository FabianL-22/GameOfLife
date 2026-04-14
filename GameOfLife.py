import sys
from subprocess import call
import time
import random
import copy
import logging

logging.basicConfig(filename='GameOfLife_log.txt', level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')
logging.disable(logging.INFO)

logging.debug('GameOfLife.py started.')

NUMBER_OF_COLS = 55
NUMBER_OF_ROWS = 25

# gives an empty screen of the size NUMBER_OF_ROWS x NUMBER_OF_COLS
def initalize_screen():

    empty_screen = []
    for i in range(NUMBER_OF_COLS):
        # empty_row has to be assigned every time to create new reference
        empty_row = [0] * NUMBER_OF_ROWS
        empty_screen.append(empty_row)

    return empty_screen

# empties the given screen
def make_screen_empty(screen):

    # iterate through the rows of the screen
    for y in range(NUMBER_OF_ROWS):
        # iterate through current row
        for x in range(NUMBER_OF_COLS):
            try:
                screen[x][y] = 0
            except IndexError:
                logging.error('Error in make_screen_empty(): wrong index.')

    return

# randomly populates the screen with given density of cells
def randomize_screen(screen, density):

    # iterate through the rows of the screen
    for y in range(NUMBER_OF_ROWS):
        # iterate through current row
        for x in range(NUMBER_OF_COLS):
            alive = 0
            if random.randint(1,100) <= density * 100:
                alive = 1
            try:
                screen[x][y] = alive
            except IndexError:
                logging.error('Error in randomize_screen(): wrong index.')

    return

def print_screen(screen):
    global generation
    
    if sys.platform.startswith('win'):
        call("cls", shell=True)
    
    print(f'GENERATION {generation}')
    
    print('┌' + '──' * NUMBER_OF_COLS +  '─┐')

    alive_cells = 0

    # iterate through the rows of the screen
    for y in range(NUMBER_OF_ROWS):
        print('│', end='')
        # iterate through current row
        for x in range(NUMBER_OF_COLS):
            try:
                if screen[x][y] == 0:
                    field = '·'
                elif screen[x][y] == 1:
                    field = '■'
                    alive_cells += 1
                else:
                    field = str(screen[x][y])
                print(' ' + field, end='')
            except IndexError:
                logging.error('Error in make_screen_empty(): wrong index.')
        print(' │', end='\n')

    print('└' + '──' * NUMBER_OF_COLS +  '─┘')
    
    # calculate density of living cells
    density = alive_cells/(NUMBER_OF_COLS * NUMBER_OF_ROWS) * 100
    print(f'Living cells: {alive_cells} / density: {density:.2f} %')

    return

def iterate_screen(screen):

    # initialize new screen as copy of current screen
    next_screen = copy.deepcopy(screen)

    # iterate through the rows of the screen
    for y in range(NUMBER_OF_ROWS):
        # iterate through current row
        for x in range(NUMBER_OF_COLS):

            # count the number of nearest neighbours
            nn = 0
            # step through nearest neighbours
            for x_nn in range(-1,2):
                for y_nn in range(-1,2):
                    if x_nn == 0 and y_nn == 0:
                        # do not count current cell as neighbour
                        continue
                    # check for boundaries
                    if x + x_nn >= 0 and x + x_nn <= (NUMBER_OF_COLS - 1) and y + y_nn >= 0 and y + y_nn <= (NUMBER_OF_ROWS - 1):

                        try:
                            nn += screen[x + x_nn][y + y_nn]
                        except IndexError:
                            logging.error(f'Error in iterate_screen(): wrong index ({x+x_nn},{y+y_nn}) while counting neighbours.')

            # apply game rules
            try:
                if screen[x][y] == 1:
                    # cell is alive
                    if nn < 2 or nn > 3:
                        # cell dies of isolation or overpopulation
                        next_screen[x][y] = 0
                elif screen[x][y] == 0:
                    # cell is dead
                    if nn == 3:
                        # new cell from reproduction
                        next_screen[x][y] = 1
            except IndexError:
                logging.error(f'Error in iterate_screen(): wrong index ({x},{y})  while applying game rules.')

    if next_screen == screen:
        logging.info('Iteration did not change state of the cellular automaton.')

    # return iterated screen
    return next_screen

#NUMBER_OF_COLS = int(input('> Number of columns: '))
#NUMBER_OF_ROWS = int(input('> Number of rows: '))

generation = 0

screen = initalize_screen()
logging.debug('Initalized the screen.')

randomize_screen(screen, 0.2)
logging.debug('Screen randomly populated.')

print_screen(screen)

logging.debug('Game of life is running now.')

while True:
    try:
        generation += 1
        screen = iterate_screen(screen)
        print_screen(screen)
        time.sleep(0.2)
    except KeyboardInterrupt:
        logging.debug('Program exited by user input.')
        sys.exit()
