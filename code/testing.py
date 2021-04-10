from shapes import Triangle, Shape, Hexagon, HShape
from shapes import hexagon_maker as hexmaker
from shapes import triangle_of_hexes as toh

import matplotlib.pyplot as plt

S1 = HShape([], [Hexagon(0,0), Hexagon(2,1)])
print(type(S1).__name__)

plottinglist = []
plottinglist.extend(S1.plot_data(color = "b-"))


axs = plt.subplot()
axs.plot(*(plottinglist))
plt.title('hexagon plot')
axs.set_aspect("equal")
plt.show()
