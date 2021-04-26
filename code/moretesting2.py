from squareshapes import Square, Polyomino, bigsquare_maker
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import ast
import time

def plotter(plottinglist, patches):
    axs = plt.subplot()
    for patch in patches:
        axs.add_patch(patch)
    axs.plot(*(plottinglist), linewidth=0.5)
    plt.autoscale(enable = True)
    axs.set_aspect("equal")
    plt.axis('off')
    plt.show()

def has_holes(config, output = False ):
    total_squares = set()
    for shape in config+[tile1]:
        total_squares = total_squares.union({(square.origin[0],square.origin[1]) for square in shape.squares})
    extended_squares = set()
    for square in total_squares:
        extended_squares = extended_squares.union({
        square,
        (square[0], square[1]-2),
        (square[0]+2, square[1]-2),
        (square[0]+2, square[1]),
        (square[0]+2, square[1]+2),
        (square[0], square[1]+2),
        (square[0]-2, square[1]+2),
        (square[0]-2, square[1]),
        (square[0]-2, square[1]-2),
        })
    without_inside = extended_squares.difference(total_squares)

    # getting a starting position
    xmin = min({coord[0] for coord in without_inside})
    ymin = min({coord[1] for coord in without_inside if coord[0] == xmin})
    mincoord = (xmin, ymin)

    # computing the connected component and removing them
    coords = { mincoord }
    while coords != set():
        without_inside = without_inside.difference(coords)
        new_coords = set()
        for coord in coords:
            nextcoords = {
            (coord[0], coord[1]-2),
            (coord[0]+2, coord[1]),
            (coord[0], coord[1]+2),
            (coord[0]-2, coord[1]),
            }
            nextcoords = {n_coord for n_coord in nextcoords if n_coord in without_inside}
            new_coords = new_coords.union(nextcoords)
        coords = new_coords

    return without_inside if output else (without_inside != set())

def tileplotter(tile, color):
    plottinglist.extend(tile.plot_data())
    for square in tile.squares:
        plot_square = RegularPolygon(square.origin, numVertices=4 ,orientation = 1/4 *np.pi, radius= np.sqrt(2), alpha=1, color= color)
        patches.append(plot_square)

def c_config_plotter(c_config):

    colordict = {
    0: "mediumaquamarine",
    1: "lightseagreen",
    2: "teal",
    3: "red",
    4: "yellow",
    }

    tileplotter(tile1, "aquamarine")

    for c_config_num  in range(len(c_config)):
        corona = c_config[c_config_num].copy()
        for tile in corona:
            tileplotter(tile, color = colordict[c_config_num])

start_time = time.time()

plottinglist = []
patches = []


""" Tile 7 with H2"""

tile1 = Polyomino(
[
Square(0, 6),
Square(2, 6),
Square(4, 6),
Square(6, 0), Square(6, 6),
Square(8, 0), Square(8, 2), Square(8, 4), Square(8, 6), Square(8, 8),
Square(10, 8),
],
priority = [
Square(6, 2), Square(6, 4),
]

)

# plottinglist.extend(tile1.plot_data())

heesch_configs = tile1.heesch_computer()


c_config = heesch_configs[0]


c_config_plotter(c_config)


print("--- %s seconds ---" % (time.time() - start_time))
plotter(plottinglist, patches)
