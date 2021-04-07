from shapes import Triangle, Shape
from shapes import hexagon_maker as hexmaker
import matplotlib.pyplot as plt


S1 = Shape([elem for elem in hexmaker(0,0) if elem != Triangle(0,0)])


plottinglist = []
for shape in S1.corona_maker(S1.orientations())[0]:
    plottinglist.extend(shape.plot_data(color = "g-"))
plt.plot(*(plottinglist+S1.plot_data()))
plt.title('hexagon plot')
plt.show()
