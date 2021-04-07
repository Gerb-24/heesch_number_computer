from shapes import Triangle, Shape
from shapes import hexagon_maker as hexmaker
import matplotlib.pyplot as plt



# fish shape
# plot_data = []
# S1 = Shape(hexmaker(0,0)+[Triangle(1,-1),  Triangle(2,1, up=False)])
# first_tri = S1.outside()[0]
# print(first_tri)
# second_tri_list =[elem for elem in S1.triangles if elem.up == first_tri.up]
# for elem in second_tri_list:
#     S2 = S1.translate(first_tri.v1[0]-elem.v1[0], first_tri.v1[1]-elem.v1[1])
#     if all(triangle not in S2.triangles for triangle in S1.triangles):
#         plot_data.extend(S2.plot_data("g-"))
# plt.plot(*(S1.plot_data()+plot_data))
# plt.show()


plot_data = []
S1 = Shape(hexmaker(0,0)+[Triangle(1,-1),  Triangle(2,1, up=False)])
outside_list = S1.outside()
while len(outside_list)>0:
    first_tri = outside_list[0]
    second_tri_list =[elem for elem in S1.triangles if elem.up == first_tri.up]
    for elem in second_tri_list:
        S2 = S1.translate(first_tri.v1[0]-elem.v1[0], first_tri.v1[1]-elem.v1[1])
        if all(triangle not in S1.triangles for triangle in S2.triangles):
            plot_data.extend(S2.plot_data("g-"))
    plt.plot(*(S1.plot_data()+plot_data))
    plt.show()


# plottinglist = []
# out_tris = S1.outside()
# new_out_tris = out_tris.copy()
# if all(triangle not in S2.triangles for triangle in S1.triangles ):
#     for tri in out_tris:
#         if tri in S2.triangles:
#             for edge in tri.edges:
#                 el = list(edge)
#                 xcoords = [el[0][0], el[1][0]]
#                 ycoords = [el[0][1]-el[0][0], el[1][1]-el[1][0]]
#                 plottinglist.extend([xcoords, ycoords, "g-"])
# else:
#     print("oops that collides")
#
#
# plt.plot(*(S1.plot_data(color="r-" )+S2.plot_data(color="b-")+plottinglist))
# plt.title('hexagon plot')
# plt.show()
