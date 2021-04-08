from shapes import Triangle, Shape
from shapes import hexagon_maker as hexmaker


S1 = Shape(hexmaker(0,0)+hexmaker(2,1)+hexmaker(3,0)+hexmaker(2,-2)+hexmaker(0,-3))

# bookkeeper = S1.corona_maker(S1.orientations(), bookkeeping=True)
# # for k in range(len(bookkeeper)):
# for k in [9]:
#     corona_lijst = bookkeeper[k]
#     #print(f" for item {k} we have a length of {len(corona_lijst)}")
#     #print(corona_lijst)
#     for i in range(len(corona_lijst)):
#         for shape in corona_lijst[i]:
#             plottinglist.extend(shape.translate(i*5,k*5).plot_data(color = "g-")+S1.translate(i*5,k*5).plot_data())
#             # for j in range(k+1):
#             #     plottinglist.extend(S1.outside()[j].translate(i*5,k*5).plot_data("r-"))



def plotting_list_writer(base):
    plottinglist = []
    for shape in base.corona_maker(base.orientations())[0]:
        plottinglist.extend(shape.plot_data(color = "g-"))
    plottinglist.extend(base.plot_data())
    with open('./plotlist.txt', 'w') as file:
        file.write(str(plottinglist))

plotting_list_writer(S1)
