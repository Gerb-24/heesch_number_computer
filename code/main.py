from shapes import Triangle, Shape
from shapes import hexagon_maker as hexmaker
import matplotlib.pyplot as plt


S1 = Shape([Triangle(0,0)])

plottinglist = []

bookkeeper = S1.corona_maker(S1.orientations())
# for k in range(len(bookkeeper)):
for k in [5]:
    corona_lijst = bookkeeper[k]
    for i in range(len(corona_lijst)):
        for shape in corona_lijst[i]:
            plottinglist.extend(shape.translate(i*5,k*5).plot_data(color = "g-")+S1.translate(i*5,k*5).plot_data())
            # for j in range(booknumber+1):
            #     plottinglist.extend(S1.outside()[j].translate(i*5,0).plot_data("r-"))

axs = plt.subplot()
axs.plot(*(plottinglist))
plt.title('hexagon plot')
axs.set_aspect("equal")
plt.show()
