from shapes import Triangle, Shape
from hexshapes import Hexagon, HShape
from shapes import hexagon_maker as hexmaker
from shapes import triangle_of_hexes as toh
from hexshapes import bighex_maker as bhmaker

import matplotlib.pyplot as plt

# S1 = HShape( [Hexagon(0,0), Hexagon(2,1), Hexagon(3,0)])
# S1 = HShape([Hexagon(0,0, [1, 0, 0, -1, 0, 0])])

H1 = Hexagon(0, 0, [1, 0, 0, 0, 0, 0])
H2 = Hexagon(1, 2, [0, 0, -1, 0, 0, 0])
S1 = HShape([H1, H2])

config = S1.corona_maker(S1.orientations())[0]

plottinglist = []
# for shape in config:
#     plottinglist.extend(shape.plot_data(color="g"))
# plottinglist.extend(S1.plot_data(color="b"))
plottinglist.extend(S1.outside_plot_data())

axs = plt.subplot()
axs.plot(*(plottinglist))
plt.title('hexagon plot')
axs.set_aspect("equal")
plt.show()
