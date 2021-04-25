from squareshapes import Square, Polyomino, bigsquare_maker
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from tiles import H3
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



tile1 = H3

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
#
# print("data is written in")

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
    possible_configs.append([config])
coronalist = [possible_config[0] for possible_config in possible_configs]
"""
In possible_configs we have all the possible corona around the base shape
We loop over all the different coronas and
use sec_corona_maker to determine all the second coronas
and then extend all the possible configurations to second_configs
"""



# def heesch_corona(possible_configs):
#     def sec_corona_maker(conf_corona):
#
#         """
#         We now translate, rotate and flip the whole config so that the start_tile
#         is the same as the base tile.
#         """
#
#         def transform(st_tile, configuration):
#
#             def flip(flipped, tile):
#
#                 """ A function that flips a tile if flipping is true,
#                 otherwise it just returns the tile """
#
#                 if flipped:
#                     return tile.flip()
#                 else:
#                     return tile
#
#             def rotate(rotation, tile):
#
#                 """ A function that can rotate a tile
#                 by 90 degrees multiple times"""
#
#                 if rotation == 0:
#                     return tile
#                 else:
#                     return rotate(rotation - 90, tile.rot_90())
#
#             def translate(translation, tile):
#
#                 """ A function that translates a tile
#                 just to keep things more organised """
#
#                 return tile.translate(*translation)
#
#             sc = st_tile.shapecode
#             translation = ( -sc["translation"][0], -sc["translation"][1])
#             flipped = sc["flipped"]
#             rotation = 360 - sc["rotation"]
#
#             transformed_config = [flip(flipped, rotate(rotation, translate(translation, tile))) for tile in configuration]
#
#             return transformed_config
#
#         """
#         Now we take a for loop over all the coronas in possible_configs
#         When this corona fits we append it to the list of the new possible configurations
#         A corona fits if all of the tiles that do collide with fixed configuration
#         are actually part of that configuration.
#         """
#
#         def collides_with(tile, configuration):
#
#             """ In here we check if a tile collides with one of the tiles in a configuration """
#
#             key_dict = {
#             "0F": 0,
#             "90F": 1,
#             "180F": 2,
#             "270F": 3,
#             "0T": 4,
#             "90T": 5,
#             "180T": 6,
#             "270T": 7,
#             }
#
#             coord = tile.shapecode["translation"]
#             pre_key = f"""{tile.shapecode["rotation"]}{"T" if tile.shapecode["flipped"] else "F"}"""
#             key = key_dict[pre_key]
#
#             for conf_tile in configuration:
#                 if coord in conf_tile.collision_data[key]:
#                     return True
#             return False
#
#         def retransform(st_tile, corona):
#
#             def flip(flipped, tile):
#
#                 """ A function that flips a tile if flipping is true,
#                 otherwise it just returns the tile """
#
#                 if flipped:
#                     return tile.flip()
#                 else:
#                     return tile
#
#             def rotate(rotation, tile):
#
#                 """ A function that can rotate a tile
#                 by 90 degrees multiple times"""
#
#                 if rotation == 0:
#                     return tile
#                 else:
#                     return rotate(rotation - 90, tile.rot_90())
#
#             def translate(translation, tile):
#
#                 """ A function that translates a tile
#                 just to keep things more organised """
#
#                 return tile.translate(*translation)
#
#             sc = st_tile.shapecode
#             translation = sc["translation"]
#             flipped = sc["flipped"]
#             rotation = sc["rotation"]
#
#             retransformed_corona = [translate(translation, rotate(rotation, flip(flipped, tile))) for tile in corona]
#
#             return retransformed_corona
#
#         """
#         new_c_configs now contains the all the possible coronas
#         around the start_tile that fit with the fixed configuration.
#         """
#
#         """
#         In the same way as we did with the corona_maker function
#         we now want to combine these with the old config to get a list of possible_c_configs
#         for every tile in the corona of the config we will now change
#         the possible_c_configs to be all of the currently possible_c_configs
#         """
#
#         # config = [tile1] + conf_corona
#         possible_c_configs = [ [conf_corona, [] ] ]
#
#         """
#         So here we loop over the tiles in the corona of the config
#         where we start at tile 1, since we already have done tile 0
#         """
#         print(f"the length of conf_corona: {len(conf_corona)}")
#         for start_num in range(len(conf_corona)):
#             start_tile = conf_corona[start_num]
#
#             """ We now go in a loop over all the c_configs in possible_c_configs """
#             new_possible_c_configs = []
#             for c_config in possible_c_configs:
#                 """
#                 Since we now want to work with c_config with corona structure
#                 we need to define something new that we want to translate
#                 which we call the absolute c config
#                 """
#                 # print(c_config[1])
#                 abs_c_config = [tile1] + c_config[0] + c_config[1]
#                 transformed_abs_c_config = transform(start_tile, abs_c_config)
#
#                 """
#                 For this recentered absoltue c_config we will append all of the
#                 retransformed corona that fit with the transformed c_config
#                 """
#
#                 new_c_configs = []
#                 for corona in possible_configs:
#                     if all(c_tile in transformed_abs_c_config for c_tile in corona if collides_with(c_tile, transformed_abs_c_config)):
#                         retransformed_corona = [ tile for tile in retransform( start_tile, corona ) if tile not in abs_c_config ]
#                         # new_c_configs.append( c_config + retransformed_corona )
#                         """
#                         We first copy the current c_config in corona structure
#                         and add the new retransformed_corona to it
#                         then we append this to new_c_configs, this then contains all the new_possible_c_configs at the end
#                         """
#                         c_config_with_added_corona = c_config.copy()
#                         c_config_with_added_corona[1] = c_config_with_added_corona[1] + retransformed_corona
#                         new_c_configs.append( c_config_with_added_corona )
#
#                 new_possible_c_configs.extend( new_c_configs )
#
#             """
#             If we no corona fits anymore for every possible c_config,
#             then the original config is dead
#             """
#
#             if new_possible_c_configs == []:
#                 possible_c_configs = []
#                 break
#
#             possible_c_configs = new_possible_c_configs.copy()
#
#         return possible_c_configs
#
#     second_configs = []
#     for conf_corona_index in range(len(possible_configs)):
#         print( f" We are at corona {conf_corona_index} out of {len(possible_configs)}  " )
#         conf_corona = possible_configs[conf_corona_index]
#
#         second_configs.extend(sec_corona_maker(conf_corona))
#     print(f"in total there are {len(second_configs)} working configurations")
#
#     return second_configs


""" This is the plotting section, where we can view the things we have created """

# second_configs = tile1.heesch_corona(possible_configs, coronalist, 0)
#
#
# second_configs_data = []
# for config in second_configs:
#     config_data = []
#     for corona in config:
#         corona_data = []
#         for tile in corona:
#             corona_data.append(tile.to_data())
#         config_data.append(corona_data)
#     second_configs_data.append(config_data)
# with open('./code/second_test_data.txt', 'w') as file:
#     file.write(str(second_configs_data))

with open('./code/second_test_data.txt', 'r') as text:
    print("Loading the second corona data...")
    second_configs_data = ast.literal_eval(text.readline())
second_configs = []
for config_data in second_configs_data:
    config = []
    for corona_data in config_data:
        corona = []
        for tile in corona_data:
            corona.append(Polyomino(
            [Square(square["x"], square["y"]) for square in shape["squares"]],
            shapecode = shape["shapecode"],
            priority = shape["priority"],
            collision_data = shape["collision_data"]
            ))
        config.append(corona)
    second_configs.append(config)
print(" the second configurations have been loaded ")

third_configs = tile1.heesch_corona(second_configs, coronalist, 1)

c_config = third_configs[0]
def c_config_plotter(c_config):
    tileplotter(tile1, "aquamarine")
    for tile in c_config[0]:
        color = "mediumaquamarine"
        tileplotter(tile, color)

    for tile in c_config[1]:
        color = "lightseagreen"
        tileplotter(tile, color)

    for tile in c_config[2]:
        color = "greenyellow"
        tileplotter(tile, color)



c_config_plotter(c_config)


print("--- %s seconds ---" % (time.time() - start_time))
plotter(plottinglist, patches)
