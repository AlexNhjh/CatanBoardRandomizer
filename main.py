import random
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import math

resource_tiles_base_game = {'sheep': 4,
                            'wheat': 4,
                            'forest': 4,
                            'stone': 3,
                            'brick': 3,
                            'desert': 1}

resource_tiles_expansion = {'sheep': 6,
                            'wheat': 6,
                            'forest': 6,
                            'stone': 5,
                            'brick': 5,
                            'desert': 2}
number_tiles_base_game = {'2':1,
                          '3':2,
                          '4':2,
                          '5':2,
                          '6':2,
                          '8':2,
                          '9':2,
                          '10':2,
                          '11':2,
                          '12':1}
number_tiles_expansion = {'2':2,
                         '3':3,
                         '4':3,
                         '5':3,
                         '6':3,
                         '8':3,
                         '9':3,
                         '10':3,
                         '11':3,
                         '12':2}

def generateRandomBoard(board_type='base_game'):
    if board_type == 'base_game':
        resource_tiles = resource_tiles_base_game
        number_tiles = number_tiles_base_game
    else:
        resource_tiles = resource_tiles_expansion
        number_tiles = number_tiles_expansion


    tiles = []
    for k,v in resource_tiles.items():
        for i in range(v):
            tiles.append(k)
    random.shuffle(tiles)

    numbers = []
    for k,v in number_tiles.items():
        for i in range(v):
            numbers.append(k)
    random.shuffle(numbers)


    tiles_left = len(tiles)
    numbers_left = len(numbers)
    row_size = 3

    direction = 'growing'
    board = []
    while tiles_left > 0:
        temp = []
        for i in range(row_size):

            if tiles[tiles_left - 1] != 'desert':
                num = numbers[numbers_left - 1]
            else:
                num = '0'

            temp.append([tiles[tiles_left - 1], str(num)])
            numbers_left -= 1
            tiles_left -= 1
        if tiles_left < len(tiles) // 2:
            direction = 'shrinking'
        if direction == 'growing':
            row_size += 1
        else:
            row_size -= 1

        board.append(temp)

    return board


def add_water(board):
    harbors = {'sheep harbor':1,
               'wheat harbor':1,
               'stone harbor':1,
               'brick harbor':1,
               'forest harbor':1,
               'generic harbor':4}

    harborList = []
    for k, v in harbors.items():
        for i in range(v):
            harborList.append(k)
    random.shuffle(harborList)

    water_tiles = [-1] * (len(board) * 2 + 8 - len(harborList))

    combined = water_tiles + harborList


    def shuffle_no_adjacent_numbers(items):
        while True:
            random.shuffle(items)
            valid = True
            for i in range(1, len(items)):
                if items[i] != -1 and items[i - 1] != -1:
                    valid = False
                    break
                if i == len(items) - 1:
                    if items[0] != -1 and items[-1] != -1:
                        valid = False
                        break
            if valid:
                return items


    shuffled_water_tiles = shuffle_no_adjacent_numbers(combined)

    for i in range(len(shuffled_water_tiles)):
        if 'harbor' in str(shuffled_water_tiles[i]):
            shuffled_water_tiles[i] = [shuffled_water_tiles[i], '-1']
        else:
            shuffled_water_tiles[i] = ['water', '0']

    for row in range(len(board)):
        board[row].insert(0, ['water','0'])
        board[row].insert(len(board[row]), ['water','0'])
    board.insert(0, [['water', '0']]*4)
    board.insert(len(board), [['water', '0']]*4)

    direction = 'right'
    row, col = 0, 0
    i = 0

    # Traverse board circularly
    while i < len(shuffled_water_tiles):
        board[row][col] = shuffled_water_tiles[i]
        i += 1

        if direction == 'right':
            if col == len(board[row]) - 1:
                direction = 'down'
                row += 1
            col += 1

        elif direction == 'left':
            if col == 0:
                direction = 'up'
                row -= 1
            else:
                col -= 1


        elif direction == 'down':
            if len(board[row+1]) > len(board[row]):
                col += 1
            else:
                col -= 1
            row += 1
            if row == len(board) - 1:
                direction = 'left'


        elif direction == 'up':
            row -= 1


    return board

board = add_water(generateRandomBoard('expansion'))

print(board)
def draw_board(board):

    fig, ax = plt.subplots(figsize=(11,11))
    fig.set_facecolor('#2C71D3')

    hex_radius = 1.12
    dx = 3/2 * hex_radius * 1.15
    dy = math.sqrt(3) * hex_radius * .85

    colors = {
        'sheep': 'lightgreen',
        'wheat': 'khaki',
        'forest': 'forestgreen',
        'stone': 'gray',
        'brick': 'firebrick',
        'desert': 'navajowhite',
        'water': '#1F00FF',
        'generic': '#e6e6e6',
        'sheep harbor':   '#1A16E9',
        'wheat harbor':   '#1A16E9',
        'stone harbor':   '#1A16E9',
        'brick harbor':   '#1A16E9',
        'forest harbor':  '#1A16E9',
        'generic harbor': '#1A16E9',
    }

    max_row_len = max(len(row) for row in board)

    for r, row in enumerate(board):
        row_len = len(row)
        offset = (max_row_len - row_len) * dx / 2  # Center this row

        for c, tile in enumerate(row):

            x = c * dx + offset
            y = -r * dy
            hex = patches.RegularPolygon((x, y), numVertices=6, radius=hex_radius,
                                         orientation=math.radians(0),
                                         facecolor=colors.get(tile[0], 'white'),
                                         edgecolor='black')
            ax.add_patch(hex)
            ax.text(x, y+.55, tile[0].split(' ')[0], ha='center', va='center', fontsize=10, weight='bold')

            if tile[1] != '0':
                ax.text(x,y, tile[1].split(' ')[0], ha='center', va='center', fontsize=10, weight='bold')
                if tile[1] != '-1':
                    num = patches.Circle((x, y), radius=hex_radius-.8,
                                        facecolor='#B88747',
                                        edgecolor='black')
                else:
                    num = patches.Circle((x, y), radius=hex_radius - .8,
                                         facecolor=colors[tile[0].split(' ')[0]],
                                         edgecolor='black')
                ax.add_patch(num)

    ax.set_xlim(-1, max_row_len * dx + 1)
    ax.set_ylim(-len(board)*dy - 1, 2)
    ax.set_aspect('equal')

    plt.axis('off')
    plt.show()


draw_board(add_water(generateRandomBoard('expansion')))