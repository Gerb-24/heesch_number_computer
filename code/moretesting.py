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
# with open('./code/test_data.txt', 'w') as file:
#     file.write(str(possible_configs_data))

"""
Here we open that file and deserialize all the data.
"""

with open('./code/test_data.txt', 'r') as text:
    print("Loading the relevant data...")
    possible_configs_data = ast.literal_eval(text.readline())
possible_configs = []
for config_data in possible_configs_data:
    config = []
    for shape in config_data:
        config.append(Polyomino(
        [Square(square["x"], square["y"]) for square in shape["squares"]],
        shapecode = shape["shapecode"],
        priority = shape["priority"],
        collision_data = shape["collision_data"]
        ))
    possible_configs.append(config)

"""
In possible_configs we have all the possible corona around the base shape
We first fix one corona and add the base shape to get a configuration
"""

conf_corona = possible_configs[25]
config = [tile1] + conf_corona
start_num = 0
start_tile = conf_corona[start_num]
print(start_tile.shapecode)

"""
We now translate, rotate and flip the whole config so that the start_tile
is the same as the base tile.
"""

def transform(st_tile, configuration):

    def flip(flipped, tile):

        """ A function that flips a tile if flipping is true,
        otherwise it just returns the tile """

        if flipped:
            return tile.flip()
        else:
            return tile

    def rotate(rotation, tile):

        """ A function that can rotate a tile
        by 90 degrees multiple times"""

        if rotation == 0:
            return tile
        else:
            return rotate(rotation - 90, tile.rot_90())

    def translate(translation, tile):

        """ A function that translates a tile
        just to keep things more organised """

        return tile.translate(*translation)

    sc = st_tile.shapecode
    translation = ( -sc["translation"][0], -sc["translation"][1])
    flipped = sc["flipped"]
    rotation = 360 - sc["rotation"]

    transformed_config = [flip(flipped, rotate(rotation, translate(translation, tile))) for tile in configuration]

    return transformed_config

transformed_config = transform(start_tile, config)

"""
Now we take a for loop over all the coronas in possible_configs
When this corona fits we append it to the list of the new possible configurations
A corona fits if all of the tiles that do collide with fixed configuration
are actually part of that configuration.
"""

def collides_with(tile, configuration):

    """ In here we check if a tile collides with one of the tiles in a configuration """

    key_dict = {
    "0F": 0,
    "90F": 1,
    "180F": 2,
    "270F": 3,
    "0T": 4,
    "90T": 5,
    "180T": 6,
    "270T": 7,
    }

    coord = tile.shapecode["translation"]
    pre_key = f"""{tile.shapecode["rotation"]}{"T" if tile.shapecode["flipped"] else "F"}"""
    key = key_dict[pre_key]

    for conf_tile in configuration:
        if coord in conf_tile.collision_data[key]:
            return True
    return False

def retransform(st_tile, corona):

    def flip(flipped, tile):

        """ A function that flips a tile if flipping is true,
        otherwise it just returns the tile """

        if flipped:
            return tile.flip()
        else:
            return tile

    def rotate(rotation, tile):

        """ A function that can rotate a tile
        by 90 degrees multiple times"""

        if rotation == 0:
            return tile
        else:
            return rotate(rotation - 90, tile.rot_90())

    def translate(translation, tile):

        """ A function that translates a tile
        just to keep things more organised """

        return tile.translate(*translation)

    sc = st_tile.shapecode
    translation = sc["translation"]
    flipped = sc["flipped"]
    rotation = sc["rotation"]

    retransformed_corona = [translate(translation, rotate(rotation, flip(flipped, tile))) for tile in corona]

    return retransformed_corona

new_c_configs = []
for corona in possible_configs:
    if all(c_tile in transformed_config for c_tile in corona if collides_with(c_tile, transformed_config)):
        retransformed_corona = [ tile for tile in retransform( start_tile, corona ) if tile not in config ]
        new_c_configs.append( retransformed_corona )
print(len(new_c_configs))

"""
new_c_configs now contains the all the possible coronas
around the start_tile that fit with the fixed configuration.
Suppose now that we take the first one and now do the same for tile number 2.
"""
c_config = config.copy()
for i in range(len(conf_corona)):
    start_num = i+1
    start_tile = conf_corona[start_num]
    c_config = c_config + new_c_configs[0]
    transformed_c_config = transform(start_tile, c_config)
    new_c_configs = []
    for corona in possible_configs:
        if all(c_tile in transformed_c_config for c_tile in corona if collides_with(c_tile, transformed_c_config)):
            retransformed_corona = [ tile for tile in retransform( start_tile, corona ) if tile not in c_config ]
            new_c_configs.append( retransformed_corona )
    print(len(new_c_configs))
    if new_c_configs == []:
        break


""" This is the plotting section, where we can view the things we have created """

for tilenum in range(len(c_config)):
    tile = c_config[tilenum]
    if tilenum == 0:
        color = "aquamarine"
    elif tilenum == start_num + 1:
        color = "yellow"
    elif tilenum < len(config):
        color = "mediumaquamarine"
    else:
        color = "lightseagreen"
    tileplotter(tile, color)

# new_c_corona = new_c_configs[0]
# for tile in new_c_corona:
#     color = "turquoise"
#     tileplotter(tile, color)


print("--- %s seconds ---" % (time.time() - start_time))
plotter(plottinglist, patches)
