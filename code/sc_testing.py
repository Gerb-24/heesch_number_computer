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

# """ Good testing H1 tile """
# tile1 = Polyomino(
# [
# Square(0,0),
# Square(2,0),
# Square(4,0),
# Square(6,0),
# Square(4,2),
# Square(4,4),
# Square(4,-2),
# ]
# )

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

coronalist = tile1.heesch_computer()[0]
for index in range(len(coronalist)):
    corona_config = coronalist[index]
    for shape in corona_config:
        plottinglist.extend(shape.plot_data())
        for square in shape.squares:
            color = "turquoise" if index % 2 == 0 else "lightseagreen"
            plot_square = RegularPolygon(square.origin, numVertices=4 ,orientation = 1/4 *np.pi, radius= np.sqrt(2), alpha=1, color= color)
            patches.append(plot_square)


# config = tile1.corona_maker(tile1.orientations(), printing= True)[20]
#
# for tile in config:
#     plottinglist.extend(tile.plot_data())
#     for square in tile.squares:
#         color = "lightseagreen"
#         plot_square = RegularPolygon(square.origin, numVertices=4 ,orientation = 1/4 *np.pi, radius= np.sqrt(2), alpha=1, color= color)
#         patches.append(plot_square)

plottinglist.extend(tile1.plot_data())
for square in tile1.squares:
    color = "turquoise"
    plot_square = RegularPolygon(square.origin, numVertices=4 ,orientation = 1/4 *np.pi, radius= np.sqrt(2), alpha=1, color= color)
    patches.append(plot_square)




print("--- %s seconds ---" % (time.time() - start_time))
plotter(plottinglist, patches)
