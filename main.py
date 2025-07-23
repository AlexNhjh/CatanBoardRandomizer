import random
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
import matplotlib.image as mpimg
import matplotlib.transforms as transforms
from CTkToolTip import *

resource_tiles_base_game = {'sheep': 4,
                            'wheat': 4,
                            'wood': 4,
                            'stone': 3,
                            'brick': 3,
                            'desert': 1}

resource_tiles_expansion = {'sheep': 6,
                            'wheat': 6,
                            'wood': 6,
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

harbors = {'sheep harbor': 1,
           'wheat harbor': 1,
           'stone harbor': 1,
           'brick harbor': 1,
           'wood harbor': 1,
           'generic harbor': 4}

colors = {
    'sheep': 'lightgreen',
    'wheat': 'khaki',
    'wood': 'forestgreen',
    'stone': 'gray',
    'brick': 'firebrick',
    'desert': 'navajowhite',
    'water': '#1F00FF',
    'generic': '#e6e6e6',
    'sheep harbor': '#1A16E9',
    'wheat harbor': '#1A16E9',
    'stone harbor': '#1A16E9',
    'brick harbor': '#1A16E9',
    'wood harbor': '#1A16E9',
    'generic harbor': '#1A16E9',
}

probabilities_2_die =   {'2':1,
                         '3':2,
                         '4':3,
                         '5':4,
                         '6':5,
                         '8':5,
                         '9':4,
                         '10':3,
                         '11':2,
                         '12':1,
                         '0':0}

def generateRandomBoard(board_type='base_game'):

    global b_type
    b_type = board_type

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

    original_tiles_length = len(tiles)
    row_size = 3

    direction = 'growing'
    board = []
    cur_row = 0
    
    def check_above_2_tiles(row, col):
        if row == 0:
            return '0','0','water','water'
        if direction == 'growing':
            try:
                above_left_tile = board[row - 1][col - 1][1] if col != 0 else '0'
                above_left_resource = board[row - 1][col - 1][0] if col != 0 else 'water'
            except:
                above_left_tile = '0'
                above_left_resource = 'water'

            try:
                above_right_tile = board[row - 1][col][1]
                above_right_resource = board[row - 1][col][0]
            except:
                above_right_tile = '0'
                above_right_resource = 'water'

        elif direction == 'shrinking':
            try:
                above_left_tile = board[row - 1][col][1]
                above_left_resource = board[row - 1][col][0]
            except:
                above_left_tile = '0'
                above_left_resource = 'water'

            try:
                above_right_tile = board[row - 1][col + 1][1]
                above_right_resource = board[row - 1][col + 1][0]
            except:
                above_right_tile = '0'
                above_right_resource = 'water'

        return above_left_tile, above_right_tile, above_left_resource, above_right_resource
    
    
    while len(tiles) > 0:
        temp = []
        for i in range(row_size):
            above_left_tile, above_right_tile, above_left_resource, above_right_resource = check_above_2_tiles(cur_row, i)
            above_left_tile_probability = probabilities_2_die[above_left_tile] if above_left_tile != '0' else 0
            above_right_tile_probability = probabilities_2_die[above_right_tile] if above_right_tile != '0' else 0

            # If adjacent_tiles is set to true, recursively place tiles until we are sure that there are no
            # resource adjacencies. Otherwise, just randomly pop from the resource stack
            if adjacent_tiles:
                tile = tiles.pop(random.randrange(len(tiles)))
                attempts = 0
                max_attempts = 10
                while (
                    (tile == above_left_resource or
                    tile == above_right_resource or
                    len(temp) > 0 and temp[-1][0] == tile)
                    and attempts < max_attempts
                ):
                    tiles.append(tile)
                    random.shuffle(tiles)
                    tile = tiles.pop()
                    attempts += 1
                if attempts >= 10:
                    return (generateRandomBoard(b_type))

            else:
                tile = tiles.pop(random.randrange(len(tiles)))

            # If tile is desert, probability is always set to 0. Otherwise, randomly pop from probability stack
            # if balanced is set to true, recursively place tiles until we have a balanced board
            if tile == 'desert':
                num = '0'
            else:
                if balanced == True:
                    num = numbers.pop(random.randrange(len(numbers)))
                    attempts = 0
                    max_attempts = 10  # Or any safe value that prevents infinite loop

                    # Avoid high-probability adjacent tiles
                    while (
                            (
                                    probabilities_2_die[str(num)] in (1,4,5) and (
                                    above_right_tile_probability == probabilities_2_die[str(num)] or
                                    above_left_tile_probability == probabilities_2_die[str(num)] or
                                    (len(temp) > 0 and probabilities_2_die[temp[-1][1]] == probabilities_2_die[str(num)])
                            )
                            ) and attempts < max_attempts
                    ):
                        numbers.append(num)
                        random.shuffle(numbers)
                        num = numbers.pop()
                        attempts += 1

                    if attempts >= 10:
                        return(generateRandomBoard(b_type))
                else:
                    num = numbers.pop(random.randrange(len(numbers)))

            temp.append([tile, str(num)])

        # adjust whether the board is growing or shrinking based on if we have already placed more than half of our tiles
        if original_tiles_length > len(tiles) * 2:
            direction = 'shrinking'

        if direction == 'growing':
            row_size += 1
        else:
            row_size -= 1
        board.append(temp)
        cur_row += 1

    return board


def add_water(board):
    harborList = []
    for k, v in harbors.items():
        for i in range(v):
            harborList.append(k)

    water_tiles = [-1] * (len(board) * 2 + 8 - len(harborList))

    combined = water_tiles + harborList

    # Ensure no harbor adjacency
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

    # change shuffled water tiles from a list to a list of lists w/
    # [tile type, tile type identifier]. identifier is a bool, harbor or not harbor
    for i in range(len(shuffled_water_tiles)):
        if 'harbor' in str(shuffled_water_tiles[i]):
            shuffled_water_tiles[i] = [shuffled_water_tiles[i], '-1']
        else:
            shuffled_water_tiles[i] = ['water', '0']

    # Place insert water tiles circularly around the board
    for row in range(len(board)):
        board[row].insert(0, ['water','0'])
        board[row].insert(len(board[row]), ['water','0'])
    board.insert(0, [['water', '0']]*4)
    board.insert(len(board), [['water', '0']]*4)

    # Traverse board circularly and place harbor tiles along with the orientation of the tile relative to the board
    #                       0--->
    #                     ^  xxx \
    #                    |  xxxx  \
    #                    |  xxxxx |
    #                     \ xxxx  |
    #                      \ xxx |
    #                       -----

    # Orientation is important to keep track of to place the harbors.
    # Since the harbors can potentially border 3 vertices but can only port on 2,
    # it is important to keep track of where they are at to correctly orient the harbors

    direction = 'right'
    row, col = 0, 0
    i = 0
    orientation = "top left corner"
    while i < len(shuffled_water_tiles):
        rowlen = len(board[row]) - 1
        match (row, col):
            case (0,0):
                orientation = "top left corner"
            case (0,c) if c != 0 and c != rowlen:
                orientation = 'top'
            case (0, c) if c == rowlen:
                orientation = "top right corner"
            case (r, c) if r < len(board) // 2 and c == rowlen:
                orientation = 'top right'
            case (r, c) if r == len(board) // 2 and c == rowlen:
                orientation = 'rightmost'
            case (r, c) if r > len(board) // 2 and r != len(board) - 1 and c == rowlen:
                orientation = 'bottom right'
            case (r, c) if r == len(board) - 1 and c == rowlen:
                orientation = 'bottom right corner'
            case (r, c) if r == len(board) - 1 and c != 0 and c != rowlen:
                orientation = 'bottom'
            case(r, 0) if r == len(board) - 1:
                orientation = 'bottom left corner'
            case(r, 0) if r > len(board) // 2:
                orientation = 'bottom left'
            case(r, 0) if r == len(board) // 2:
                orientation = 'leftmost'
            case(r, 0) if r < len(board) // 2 and r != 0:
                orientation = 'top left'

        board[row][col] = shuffled_water_tiles[i] + [orientation]
        i += 1

        # Update direction of travel to match the exterior rim of the board where we placed the water tiles
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


def plot_board(board):

    fig, ax = plt.subplots(figsize=(11,11))
    fig.set_facecolor('#2C71D3')
    ax.title.set_text(f'Randomized Catan Board\n {b_type.upper()}')
    ax.title.set_fontsize(18)
    ax.title.set_fontfamily('Times New Roman')
    ax.title.set_position((.44,100))

    hex_radius = 1.12
    dx = 3/2 * hex_radius * 1.15
    dy = math.sqrt(3) * hex_radius * .85

    max_row_len = max(len(row) for row in board)

    for r, row in enumerate(board):
        row_len = len(row)
        offset = (max_row_len - row_len) * dx / 2  # Center this row

        for c, tile in enumerate(row):
            current_tile = tile[0].split(' ')[0]
            x = c * dx + offset
            y = -r * dy

            if 'harbor' not in tile[0]:
                img = mpimg.imread(f'{current_tile}.png')
                rotation_deg = 27

            # Harbor Tile. Determine rotation of tile
            else:
                img = mpimg.imread(f'bridge.png')
                match tile[2]:
                    case 'top left corner':
                        rotation_deg = 60
                    case 'top':
                        rotation_deg = random.choice([0, 60])
                    case 'top right corner':
                        rotation_deg = 0
                    case 'top right':
                        rotation_deg = random.choice([300, 0])
                    case 'rightmost':
                        rotation_deg = 300
                    case 'bottom right':
                        rotation_deg = random.choice([240, 300])
                    case 'bottom right corner':
                        rotation_deg = 240
                    case 'bottom':
                        rotation_deg = random.choice([180, 240])
                    case 'bottom left corner':
                        rotation_deg = 180
                    case 'bottom left':
                        rotation_deg = random.choice([120, 180])
                    case 'leftmost':
                        rotation_deg = 120
                    case 'top left':
                        rotation_deg = random.choice([60, 120])

            transform = transforms.Affine2D().rotate_deg_around(x, y, rotation_deg) + ax.transData

            hex = patches.RegularPolygon(
                (x, y),
                numVertices=6,
                radius=hex_radius,
                orientation=math.radians(0),
                edgecolor='#d8b960',
                linewidth=4,
                facecolor='none',
                transform=ax.transData
            )
            im = ax.imshow(
                img,
                extent=[x - hex_radius, x + hex_radius, y - hex_radius, y + hex_radius],
                zorder=0,
                transform=transform
            )
            im.set_clip_path(hex)
            ax.add_patch(hex)


            if tile[1] != '0':
                if tile[1] != '-1':
                    current_digit = tile[1].split(' ')[0]
                    current_probability = int(probabilities_2_die[current_digit])

                    # Add digit and probability to a circle patch in the center of the hexagon
                    ax.text(x, y, current_digit, ha='center', va='center', fontsize=12, weight='bold')
                    ax.text(x, y-.1, "." * current_probability,
                            ha='center', va='center',
                            fontsize=15,
                            weight='bold',
                            color=('red' if current_probability == 5 else 'black'))
                    num = patches.Circle((x, y), radius=hex_radius-.7,
                                        facecolor='#B88747',
                                        edgecolor='black')
                    ax.add_patch(num)

                elif tile[1] == '-1':  # Harbor tile
                    tile_type = tile[0].split(' ')[0]
                    tile_path = mpimg.imread(f"{tile_type}_material.png")

                    # Show image centered at (x, y)
                    tile_image = ax.imshow(
                        tile_path,
                        extent=[x - hex_radius*.27, x + hex_radius*.27, y - hex_radius*.27, y + hex_radius*.27],
                        zorder=0
                    )

                    # Clip the image to a circle
                    clip_circle = patches.Circle((x, y), radius=hex_radius - 0.8, transform=ax.transData)
                    tile_image.set_clip_path(clip_circle)
                    ax.add_patch(patches.Circle((x, y), radius=hex_radius - 0.8,
                                                facecolor='none', edgecolor='black', linewidth=1.5))

                    # Add harbor ratio text
                    ratio_text = "3:1" if 'generic' in tile[0] else "2:1"
                    ax.text(x, y, ratio_text, ha='center', va='center', fontsize=10, weight='bold')

    ax.set_xlim(-1, max_row_len * dx + 1)
    ax.set_ylim(-len(board)*dy - 1, 2)
    ax.set_aspect('equal')
    plt.axis('off')
    return fig


# Setup customtkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

canvas_widget = None  # No plot shown by default

# Create main window
window = ctk.CTk()
window.title("Matplotlib in CustomTkinter")
window.geometry("1000x1000")
window.configure(fg_color='#2C71D3')

# Create a frame to contain the canvas (to avoid covering buttons)
canvas_frame = ctk.CTkFrame(master=window, width=1000, height=1000, fg_color="transparent")
canvas_frame.place(x=0, y=0)


def show_plot(game_type, harbors):
    global canvas_widget
    if harbors:
        fig = plot_board(add_water(generateRandomBoard(game_type)))
    elif not harbors:
        fig = plot_board(generateRandomBoard(game_type))

    # Destroy old canvas if needed
    if canvas_widget:
        canvas_widget.get_tk_widget().destroy()

    # Embed new canvas inside the frame
    canvas_widget = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().place(x=0, y=0)


# Buttons (placed after canvas, and directly on the root window)
plotHarbors = False
balanced = False
adjacent_tiles = False

plot_base_game = ctk.CTkButton(window, text="Base Game", command=lambda: show_plot('base_game', plotHarbors), fg_color='black')
plot_base_game.place(x=20, y=10)

plot_expansion = ctk.CTkButton(window, text="Expansion", command=lambda: show_plot('expansion', plotHarbors), fg_color='black')
plot_expansion.place(x=20, y=50)

plot_harbors = ctk.CTkCheckBox(window, text="Randomize Harbors?", command=lambda: toggle_harbors(plotHarbors), fg_color='black')
plot_harbors.place(x=20, y=90)

balance_board = ctk.CTkCheckBox(window, text="Balance Board?", command=lambda: toggle_balance(balanced), fg_color='black')
balance_board.place(x=20, y=120)

probability_tooltip = CTkToolTip(balance_board, delay=0.0, message="No adjacent 6/8, 3,8, or 2,12 probability pairs")

toggle_adjacent_tiles_button = ctk.CTkCheckBox(window, text="Adjacent Resources?", command=lambda: toggle_adjacent_resources(adjacent_tiles), fg_color='black')
toggle_adjacent_tiles_button.place(x=20, y=150)

adjacency_tooltip = CTkToolTip(toggle_adjacent_tiles_button, delay=0.0, message="No adjacent resource tiles of the same type")

def toggle_harbors(h):
    global plotHarbors
    plotHarbors = plot_harbors.get()

def toggle_balance(h):
    global balanced
    balanced = balance_board.get()

def toggle_adjacent_resources(h):
    global adjacent_tiles
    adjacent_tiles = toggle_adjacent_tiles_button.get()

window.mainloop()