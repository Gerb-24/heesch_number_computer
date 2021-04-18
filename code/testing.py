from squareshapes import Square, Polyomino
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np

def plotter(plottinglist, patches):
    axs = plt.subplot()
    for patch in patches:
        axs.add_patch(patch)
    axs.plot(*(plottinglist), linewidth=0.5)
    plt.autoscale(enable = True)
    axs.set_aspect("equal")
    plt.axis('off')
    plt.show()

plottinglist = []
patches = []

""" Good testing H1 tile """
# tile = Polyomino(
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

tile = Polyomino(
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

coronalist = tile.heesch_computer()[0]
for index in range(len(coronalist)):
    corona_config = coronalist[index]
    for shape in corona_config:
        plottinglist.extend(shape.plot_data())
        for square in shape.squares:
            color = "turquoise" if index % 2 == 0 else "lightseagreen"
            plot_square = RegularPolygon(square.origin, numVertices=4 ,orientation = 1/4 *np.pi, radius= np.sqrt(2), alpha=1, color= color)
            patches.append(plot_square)

# corona = tile.corona_maker(tile.orientations())[0]
# for shape in corona:
#     plottinglist.extend(shape.plot_data())
#     for square in shape.squares:
#         plot_square = RegularPolygon(square.origin, numVertices=4 ,orientation = 1/4 *np.pi, radius= np.sqrt(2), alpha=1, color= "lightseagreen")
#         patches.append(plot_square)


plottinglist.extend(tile.plot_data())
for square in tile.squares:
    color = "lightseagreen"
    plot_square = RegularPolygon(square.origin, numVertices=4 ,orientation = 1/4 *np.pi, radius= np.sqrt(2), alpha=1, color= color)
    patches.append(plot_square)
plotter(plottinglist, patches)
