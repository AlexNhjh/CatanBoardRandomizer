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
    harbors = {'sheep':1,
               'wheat':1,
               'stone':1,
               'brick':1,
               'wood':1,
               'generic':4}
    harborList = []
    for k, v in harbors.items():
        for i in range(v):
            harborList.append(k)
    random.shuffle(harborList)

    harborList.insert(0, '-1')

    water_tiles = [-1] * (len(board) * 2 + 8)
    for i in range(len(water_tiles)):
        if (i % 2) == 1:
            water_tiles[i] = harborList.pop()
    print(water_tiles)

    for row in range(len(board)):
        t = water_tiles.pop()

        board[row].insert(0, ['water',t])
        board[row].insert(len(board[row]), ['water',t])

    temp = []
    for i in range(len(board[0]) - 1):
        temp.append(['water',water_tiles.pop()])
    board.insert(0, temp)
    board.insert(len(board), [['water', water_tiles.pop()]] * (len(board[len(board) - 1]) - 1))

    rowStart = random.randint(1, len(board) - 1)

    while rowStart > 1:
        print(rowStart)
        rowStart -= 1

    return board

board = add_water(generateRandomBoard('base_game'))

def draw_board(board):

    fig, ax = plt.subplots(figsize=(19, 19))
    fig.set_facecolor('#2C71D3')

    hex_radius = 1
    dx = 3/2 * hex_radius * 1.15
    dy = math.sqrt(3) * hex_radius * .85

    colors = {
        'sheep': 'lightgreen',
        'wheat': 'khaki',
        'forest': 'forestgreen',
        'stone': 'gray',
        'brick': 'firebrick',
        'desert': 'navajowhite',
        'water': 'blue'
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
            ax.text(x, y+.4, tile[0], ha='center', va='center', fontsize=10, weight='bold')
            if tile[1] != '0':
                ax.text(x,y, tile[1], ha='center', va='center', fontsize=10, weight='bold')
                num = patches.Circle((x, y), radius=hex_radius-.75,
                                      facecolor='#B88747',
                                      edgecolor='black')
                ax.add_patch(num)

    ax.set_xlim(-1, max_row_len * dx + 1)
    ax.set_ylim(-len(board)*dy - 1, 2)
    ax.set_aspect('equal')

    plt.axis('off')
    plt.show()

draw_board(board)

