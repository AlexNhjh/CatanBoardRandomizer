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

def generateRandomBoard(board_type):
    tiles = []
    for k,v in board_type.items():
        for i in range(v):
            tiles.append(k)
    random.shuffle(tiles)

    tiles_left = len(tiles)
    row_size = 3

    direction = 'growing'
    board = []
    while tiles_left > 0:
        temp = []
        for i in range(row_size):
            temp.append(tiles[tiles_left - 1])

            tiles_left -= 1
        if tiles_left < len(tiles) // 2:
            direction = 'shrinking'
        if direction == 'growing':
            row_size += 1
        else:
            row_size -= 1

        board.append(temp)

    return board



def draw_board(board):
    fig, ax = plt.subplots(figsize=(15, 15))
    hex_radius = 1
    dx = 3/2 * hex_radius * 1.15
    dy = math.sqrt(3) * hex_radius * .85

    colors = {
        'sheep': 'lightgreen',
        'wheat': 'khaki',
        'forest': 'forestgreen',
        'stone': 'gray',
        'brick': 'firebrick',
        'desert': 'navajowhite'
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
                                         facecolor=colors.get(tile, 'white'),
                                         edgecolor='black')
            ax.add_patch(hex)
            ax.text(x, y, tile, ha='center', va='center', fontsize=10, weight='bold')

    ax.set_xlim(-1, max_row_len * dx + 1)
    ax.set_ylim(-len(board)*dy - 1, 2)
    ax.set_aspect('equal')
    plt.axis('off')
    plt.show()

draw_board(generateRandomBoard(resource_tiles_base_game))

