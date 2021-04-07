from shapes import Triangle, Shape
from shapes import hexagon_maker as hexmaker
import matplotlib.pyplot as plt


S1 = Shape(hexmaker(0,0)+[Triangle(1,-1),  Triangle(2,1, up=False)])


# plottinglist = []
# for shape in S1.corona_maker(S1)[0]:
#     plottinglist.extend(shape.plot_data(color = "g-"))



plt.plot(*(S1.turn60().plot_data(color="r-" )))
plt.title('hexagon plot')
plt.show()
