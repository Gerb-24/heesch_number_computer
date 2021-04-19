from squareshapes import Square, Polyomino
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
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

start_time = time.time()

plottinglist = []
patches = []

""" Good testing H1 tile """
tile1 = Polyomino(
[
Square(0,0),
Square(2,0),
Square(4,0),
Square(6,0),
Square(4,2),
Square(4,4),
Square(4,-2),
]
)

# translation = (6,0)
# tile2 = tile1.flip().rot_90().rot_90()
# tile3 = tile1.rot_90().rot_90().translate(*translation)
# print(tile1.collisions()[1])
# print(translation in tile2.collisions()[2])
#
# for tile in [tile2, tile3]:
#     plottinglist.extend(tile.plot_data())
#     for square in tile.squares:
#         color = "turquoise" if tile == tile2 else "lightseagreen"
#         plot_square = RegularPolygon(square.origin, numVertices=4 ,orientation = 1/4 *np.pi, radius= np.sqrt(2), alpha=1, color= color)
#         patches.append(plot_square)

# coronalist = tile.heesch_computer()[0]
# for index in range(len(coronalist)):
#     corona_config = coronalist[index]
#     for shape in corona_config:
#         plottinglist.extend(shape.plot_data())
#         for square in shape.squares:
#             color = "turquoise" if index % 2 == 0 else "lightseagreen"
#             plot_square = RegularPolygon(square.origin, numVertices=4 ,orientation = 1/4 *np.pi, radius= np.sqrt(2), alpha=1, color= color)
#             patches.append(plot_square)
#

config = tile1.corona_maker(tile1.orientations(), printing= True)[20]

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
