from shapes import Triangle, Shape
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
        for shape in base.corona_maker(base.orientations())[5]:
            plottinglist.extend(shape.plot_data(color = "g-"))
    elif type == "boundary":
        for triangle in base.inside_remover():
            plottinglist.extend(triangle.plot_data("g-"))
    plottinglist.extend(base.plot_data())
    with open('./plotlist.txt', 'w') as file:
        file.write(str(plottinglist))


S1 = Shape(toh())
plotting_list_writer(S1, type = "corona")
