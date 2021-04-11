from shapes import Triangle, Shape, Hexagon, HShape
from shapes import hexagon_maker as hexmaker
from shapes import bighex_maker
from shapes import triangle_of_hexes as toh

#import matplotlib.pyplot as plt

#S1 = HShape( [Hexagon(0,0), Hexagon(2,1), Hexagon(3,0)])
S1 = HShape([Hexagon(0,0)])


# plottinglist = []
# plottinglist.extend(S1.plot_data())
# plottinglist.extend(S1.translate(8,0).plot_data())
#
#
# axs = plt.subplot()
# axs.plot(*(plottinglist))
# plt.title('hexagon plot')
# axs.set_aspect("equal")
# plt.show()
