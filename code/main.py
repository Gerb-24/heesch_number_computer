from shapes import Triangle, Shape, Hexagon, HShape
from shapes import hexagon_maker as hexmaker
from shapes import triangle_of_hexes as toh

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
        print("im struggling here")
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


# S1 = Shape(toh())
# S1 = Shape(toh() + hexmaker(2,-5) + hexmaker(5, -2) + hexmaker(6, -3))
# S1 = Shape([triangle for triangle in toh() if triangle not in hexmaker(3,-3)+hexmaker(2,-2)])
# S1 = Shape([triangle for triangle in hexmaker(0,0)+[Triangle(1,1)] if triangle not in [Triangle(0,0)]])
S2 = HShape( [Hexagon(0,0), Hexagon(2,1), Hexagon(3,0)])

""" This has types:
    1) Corona
    2) Boundary
    3) Base
"""
plotting_list_writer(S2, type = "corona")
