import random
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import math
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk

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
    # [tile type, tile type identifier]
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

    # Traverse board circularly and place harbor tiles
    #                       ---->
    #                     ^  xxx \
    #                    |  xxxx  \
    #                    |  xxxxx |
    #                     \ xxxx  |
    #                      \ xxx |
    #                       -----


    # Orientation is important to keep track of to place the harbors.
    # Since the harbors can potentially border 3 vertices but can only port on 2,
    # it is important to keep track of where they are at to correctly orient the harbors
    #
    #
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
        #print(row, col, orientation)


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


    fig, ax = plt.subplots(figsize=(11,11))
    fig.set_facecolor('#2C71D3')
    ax.title.set_text(f'Randomized Catan Board\n {board_type.upper()}')
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

            x = c * dx + offset
            y = -r * dy
            hex = patches.RegularPolygon((x, y), numVertices=6, radius=hex_radius,
                                         orientation=math.radians(0),
                                         facecolor=colors.get(tile[0], 'white'),
                                         edgecolor='black')
            ax.add_patch(hex)
            ax.text(x, y+.55, tile[0].split(' ')[0], ha='center', va='center', fontsize=10, weight='bold')

            if tile[1] != '0':

                if tile[1] != '-1':
                    ax.text(x, y, tile[1].split(' ')[0], ha='center', va='center', fontsize=10, weight='bold')
                    num = patches.Circle((x, y), radius=hex_radius-.8,
                                        facecolor='#B88747',
                                        edgecolor='black')
                elif tile[1] == '-1':  # Harbor tile
                    num = patches.Circle((x, y), radius=hex_radius - .8,
                                     facecolor=colors[tile[0].split(' ')[0]],
                                     edgecolor='black')

                    if 'generic' in tile[0]:
                        ax.text(x, y, "3:1", ha='center', va='center', fontsize=10, weight='bold')
                    else:
                        ax.text(x, y, "2:1", ha='center', va='center', fontsize=10, weight='bold')
                    corners = []

                    # Function and for loop to plot tick marks on the hexagons via ChatGPT.
                    for i in range(6):
                        angle_deg = 60 * i - 30
                        angle_rad = math.radians(angle_deg)
                        cx = x + hex_radius * math.cos(angle_rad)
                        cy = y + hex_radius * math.sin(angle_rad)
                        corners.append((cx, cy))

                    def draw_tick(corner_x, corner_y, center_x, center_y, length=0.2):
                        vx = corner_x - center_x
                        vy = corner_y - center_y
                        norm = math.sqrt(vx ** 2 + vy ** 2)
                        vx /= norm
                        vy /= norm
                        ex = corner_x - vx * length * 4
                        ey = corner_y - vy * length * 4
                        ax.plot([corner_x, ex], [corner_y, ey], color=colors[tile[0].split(' ')[0]], linewidth=5)


                    # Corner indeces of harbor tiles
                    #                     2
                    #                     *
                    #           3     *   *   *      1
                    #             *   *   *   *   *
                    #             *   *   *   *   *
                    #             *   *   *   *   *
                    #           4     *   *   *      0
                    #                     *
                    #                     5
                    #
                    c1, c2 = 0, 0
                    match tile[2]:
                        case 'top left corner':
                            c1 = 0
                            c2 = 5
                        case 'top':
                            c1 = 5
                            c2 = random.choice([0,4])
                        case 'top right corner':
                            c1 = 4
                            c2 = 5
                        case 'top right':
                            c1 = 4
                            c2 = random.choice([3,5])
                        case 'rightmost':
                            c1 = 4
                            c2 = 3
                        case 'bottom right':
                            c1 = 3
                            c2 = random.choice([2,4])
                        case 'bottom right corner':
                            c1 = 2
                            c2 = 3
                        case 'bottom':
                            c1 = 2
                            c2 = random.choice([3,1])
                        case 'bottom left corner':
                            c1 = 1
                            c2 = random.choice([2,0])
                        case 'bottom left':
                            c1 = 1
                            c2 = random.choice([2,0])
                        case 'leftmost':
                            c1 = 1
                            c2 = 0
                        case 'top left':
                            c1 = 0
                            c2 = random.choice([1,5])


                    draw_tick(*corners[c1], x, y)
                    draw_tick(*corners[c2], x, y)

                ax.add_patch(num)


    ax.set_xlim(-1, max_row_len * dx + 1)
    ax.set_ylim(-len(board)*dy - 1, 2)
    ax.set_aspect('equal')

    plt.axis('off')
    return fig






# Setup customtkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

canvas_widget = None  # global to manage redrawing

# Create main window
window = ctk.CTk()
window.title("Matplotlib in CustomTkinter")
window.geometry("800x800")
window.configure(fg_color='#2C71D3')
# Create a frame to contain the canvas (to avoid covering buttons)
canvas_frame = ctk.CTkFrame(master=window, width=800, height=800, fg_color="transparent")
canvas_frame.place(x=0, y=0)

def show_plot(game_type):
    global canvas_widget
    fig = generateRandomBoard(game_type)

    # Destroy old canvas if needed
    if canvas_widget:
        canvas_widget.get_tk_widget().destroy()

    # Embed new canvas inside the frame
    canvas_widget = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().place(x=0, y=0)

# Buttons (placed *after* canvas, and directly on the root window)
plot_base_game = ctk.CTkButton(window, text="Base Game", command=lambda: show_plot('base_game'), fg_color='black')
plot_base_game.place(x=20, y=10)

plot_expansion = ctk.CTkButton(window, text="Expansion", command=lambda: show_plot('expansion'), fg_color='black')
plot_expansion.place(x=20, y=50)

window.mainloop()

