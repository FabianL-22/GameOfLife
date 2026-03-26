import sys
import time
import random
import copy

NUMBER_OF_COLS = 50
NUMBER_OF_ROWS = 20

#screen = [['  ']*NUMBER_OF_COLS]*NUMBER_OF_ROWS

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
                print('Fehler in make_screen_empty(): Falscher Index.')

#    row = ['  ' for i in range(NUMBER_OF_COLS)]
#    screen = [row for i in range(NUMBER_OF_ROWS)]

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
                print('Fehler in randomize_screen(): Falscher Index.')

    return

def print_screen(screen):
    print('__' * NUMBER_OF_COLS + '_')

    alive_cells = 0

    # iterate through the rows of the screen
    for y in range(NUMBER_OF_ROWS):
        # iterate through current row
        for x in range(NUMBER_OF_COLS):
            try:
                if screen[x][y] == 0:
                    field = ' '
                elif screen[x][y] == 1:
                    field = '■'
                    alive_cells += 1
                else:
                    field = str(screen[x][y])
                print('|' + field, end='')
            except IndexError:
                print('Fehler in make_screen_empty(): Falscher Index.')
        print('|', end='\n')

    print('__' * NUMBER_OF_COLS + '_')
    density = alive_cells/(NUMBER_OF_COLS * NUMBER_OF_ROWS) * 100
    print('Living cells: ' + str(alive_cells) + ' / density: ' + format(density, '.2f')+ ' %')

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
                            print('Fehler in iterate_screen(): Falscher Index (' + str(x+x_nn) + ',' + str(y+y_nn) + ') beim Zählen der Nachbarn.')

            # apply game rules
            try:
                if screen[x][y] == 1:
                    #print('Cell at (' + str(x) + ',' + str(y) + ') has ' + str(nn) + ' neighbours', end='')
                    # cell is alive
                    if nn < 2 or nn > 3:
                        # cell dies of isolation or overpopulation
                        next_screen[x][y] = 0
                        #print(' - dies.')
                    #else:
                        #print(' - nothing happens.')
                elif screen[x][y] == 0:
                    #print('No cell at (' + str(x) + ',' + str(y) + ') with ' + str(nn) + ' neighbours', end='')
                    # cell is dead
                    if nn == 3:
                        # new cell from reproduction
                        next_screen[x][y] = 1
                        #print(' - new cell is created.')
                    #else:
                        #print(' - nothing happens.')
            except IndexError:
                print('Fehler in iterate_screen(): Falscher Index.')

    if next_screen == screen:
        print('Nothing happened.')

    # return iterated screen
    return next_screen

#NUMBER_OF_COLS = int(input('> Number of columns: '))
#NUMBER_OF_ROWS = int(input('> Number of rows: '))

screen = initalize_screen()

randomize_screen(screen, 0.6)
print_screen(screen)

while True:
    try:
        screen = iterate_screen(screen)
        print_screen(screen)
        time.sleep(0.4)
    except KeyboardInterrupt:
        sys.exit()
