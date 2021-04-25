from squareshapes import Square, Polyomino, bigsquare_maker
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from tiles import T2H2
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



start_time = time.time()

plottinglist = []
patches = []



tile1 = T2H2

"""
With this commented part we can write all the first corona data to a file
called test_data.txt. This is useful when testing,
so that we do not have to recalculate all the data for the first coronas.
"""
# possible_config = tile1.corona_maker(tile1.orientations(), printing= True)
# print("now removing holes")
# nh_possible_config = [config for config in possible_config if not has_holes(config)]
# print(len(nh_possible_config))
# possible_configs_data = []
# for config in nh_possible_config:
#     config_data = []
#     for shape in config:
#         config_data.append(shape.to_data())
#     possible_configs_data.append(config_data)
# with open('./code/T2H2_first_corona_data.txt', 'w') as file:
#     file.write(str(possible_configs_data))
#
# print("data is written in")

"""
Here we open that file and deserialize all the data.
"""

# with open('./code/T2H2_first_corona_data.txt', 'r') as text:
#     print("Loading the relevant data...")
#     possible_configs_data = ast.literal_eval(text.readline())
# possible_configs = []
# for config_data in possible_configs_data:
#     config = []
#     for shape in config_data:
#         config.append(Polyomino(
#         [Square(square["x"], square["y"]) for square in shape["squares"]],
#         shapecode = shape["shapecode"],
#         priority = shape["priority"],
#         collision_data = shape["collision_data"]
#         ))
#     possible_configs.append([config])
# coronalist = [possible_config[0] for possible_config in possible_configs]

heesch_configs = tile1.heesch_computer()


c_config = heesch_configs[0]
def c_config_plotter(c_config):
    tileplotter(tile1, "aquamarine")
    for tile in c_config[0]:
        color = "mediumaquamarine"
        tileplotter(tile, color)

    for tile in c_config[1]:
        color = "lightseagreen"
        tileplotter(tile, color)

    # for tile in c_config[2]:
    #     color = "greenyellow"
    #     tileplotter(tile, color)



c_config_plotter(c_config)


print("--- %s seconds ---" % (time.time() - start_time))
plotter(plottinglist, patches)
