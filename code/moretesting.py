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

start_time = time.time()

plottinglist = []
patches = []



""" Tile 2 with H2"""
priority = [
Square(2,0),
Square(4,6),
]

tile1 = Polyomino(
[
Square(0,0),
Square(0,2),
Square(0,4),
Square(0,6),
Square(-2,4),
Square(2,2),
Square(2,4),
Square(2,6),
Square(4,0),
Square(4,2),
Square(4,6),
],
priority = priority
)

possible_config = tile1.corona_maker(tile1.orientations(), printing= True)
print("now removing holes")
nh_possible_config = [config for config in possible_config if not has_holes(config)]
print(len(nh_possible_config))
config = nh_possible_config[10]
config_data = []
for shape in config:
    config_data.append(shape.to_data())
with open('./code/test_data.txt', 'w') as file:
    file.write(str(config_data))

# with open('./code/test_data.txt', 'r') as text:
#     data = ast.literal_eval(text.readline())
# config = []
# for shape in data:
#     config.append(Polyomino(
#     [Square(square["x"], square["y"]) for square in shape["squares"]],
#     shapecode = shape["shapecode"],
#     priority = shape["priority"],
#     collision_data = shape["collision_data"]
#     ))



for tile in config:
    plottinglist.extend(tile.plot_data())
    for square in tile.squares:
        color = "lightseagreen"
        plot_square = RegularPolygon(square.origin, numVertices=4 ,orientation = 1/4 *np.pi, radius= np.sqrt(2), alpha=1, color= color)
        patches.append(plot_square)

plottinglist.extend(tile1.plot_data())
for square in tile1.squares:
    color = "turquoise"
    plot_square = RegularPolygon(square.origin, numVertices=4 ,orientation = 1/4 *np.pi, radius= np.sqrt(2), alpha=1, color= color)
    patches.append(plot_square)




print("--- %s seconds ---" % (time.time() - start_time))
plotter(plottinglist, patches)
