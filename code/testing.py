from squareshapes import Square
import matplotlib.pyplot as plt

def plotter(plottinglist):
    axs = plt.subplot()
    axs.plot(*(plottinglist), linewidth=0.3)
    plt.autoscale(enable = True)
    axs.set_aspect("equal")
    plt.axis('off')
    plt.show()

square = Square(2,4)

plottinglist = []
plottinglist.extend(square.plot_data())

plotter(plottinglist)
