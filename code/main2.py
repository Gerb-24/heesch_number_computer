import ast
import matplotlib.pyplot as plt

with open('./code/plotlist.txt', 'r') as text:
    plottinglist = ast.literal_eval(text.readline())

    axs = plt.subplot()
    axs.plot(*(plottinglist))
    plt.title('hexagon plot')
    axs.set_aspect("equal")
    plt.show()
