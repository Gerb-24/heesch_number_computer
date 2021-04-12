from shapes import Triangle, Shape
from hexshapes import Hexagon, HShape
from shapes import hexagon_maker as hexmaker
from shapes import triangle_of_hexes as toh
from hexshapes import bighex_maker as bhmaker
import time

def bookkeeper_plotting_list(base):
    plottinglist = []
    bookkeeper = base.corona_maker(base.orientations(), bookkeeping=True)
    # for k in range(len(bookkeeper)):
    for k in [9]:
        corona_lijst = bookkeeper[k]
        #print(f" for item {k} we have a length of {len(corona_lijst)}")
        #print(corona_lijst)
        for i in range(len(corona_lijst)):
            for shape in corona_lijst[i]:
                plottinglist.extend(shape.translate(i*5,k*5).plot_data(color = "g-")+base.translate(i*5,k*5).plot_data())
                # for j in range(k+1):
                #     plottinglist.extend(S1.outside()[j].translate(i*5,k*5).plot_data("r-"))
    return plottinglist

def plotting_list_writer(base, type = "corona"):
    plottinglist = []
    if type == "corona":
        coronalist = base.corona_maker(base.orientations())[0]
        for shape in coronalist:
            plottinglist.extend(shape.plot_data(color = "g-"))
    elif type == "boundary":
        for triangle in base.inside_remover():
            plottinglist.extend(triangle.plot_data("g-"))
    elif type == "base":
        pass
    plottinglist.extend(base.plot_data())
    with open('./plotlist.txt', 'w') as file:
        file.write(str(plottinglist))


start_time = time.time()

""" Some testing shapes"""
# S1 = Shape(toh())
# S1 = Shape(toh() + hexmaker(2,-5) + hexmaker(5, -2) + hexmaker(6, -3))
# S1 = Shape([triangle for triangle in toh() if triangle not in hexmaker(3,-3)+hexmaker(2,-2)])
# S1 = Shape([triangle for triangle in hexmaker(0,0)+[Triangle(1,1)] if triangle not in [Triangle(0,0)]])
# S1 = Shape(hexmaker(-1,1)+hexmaker(1,2)+hexmaker(2,1)+hexmaker(1,-1)+hexmaker(-1,-2))

S1 = HShape([Hexagon(0,0, [1, 0, 0, -1, 0, 0])])
# S1 = HShape( [Hexagon(0,0), Hexagon(2,1), Hexagon(3,0)])
# S1 = HShape( [hex for hex in bhmaker(0,0) if hex not in [Hexagon(-2,-1), Hexagon(0,0)] ]  )
# S1 = HShape( bhmaker(0,0)+[Hexagon(-2,2), Hexagon(-2,-4), Hexagon(4,2), Hexagon(0,-3), Hexagon(3,0), Hexagon(4,-1)] )


""" This has types:
    1) Corona
    2) Boundary
    3) Base
"""
plotting_list_writer(S1, type = "corona")
print("--- %s seconds ---" % (time.time() - start_time))
