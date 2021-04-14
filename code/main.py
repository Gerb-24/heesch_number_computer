from shapes import Triangle, Shape
from hexshapes import Hexagon, HShape
from shapes import hexagon_maker as hexmaker
from shapes import triangle_of_hexes as toh
from hexshapes import bighex_maker as bhmaker
import time

def data_writer(base, type = "corona"):
    with open('./code/plotlist.txt', 'w') as file:
        if type == "heesch":
            coronalist = base.heesch_computer()[0]
            coronadata = []
            for corona_config in coronalist:
                coronadata.append([shape.to_data() for shape in corona_config])
            datadict = {"type": type, "num": len(coronalist), "data": {"base": base.to_data(), "heesch": coronadata}}

        elif type == "corona2":
            coronalist = base.second_corona()[0]
            first_data = []
            for shape in coronalist["first"]:
                first_data.append(shape.to_data())
            second_data = []
            for shape in coronalist["second"][0]:
                second_data.append(shape.to_data())
            datadict = {"type": type, "data": {"base": base.to_data(), "first": first_data, "second": second_data}}

        elif type == "corona":
            coronalist = base.corona_maker(base.orientations())[0]
            corona_data = []
            for shape in coronalist:
                corona_data.append(shape.to_data())
            datadict = {"type": type, "data": {"base": base.to_data(), "corona": corona_data}}

        elif type == "base":
            datadict = {"type": type, "data": {"base": base.to_data()}}

        file.write(str(datadict))

start_time = time.time()

""" Some testing shapes"""
# S1 = Shape(toh())
# S1 = Shape(toh() + hexmaker(2,-5) + hexmaker(5, -2) + hexmaker(6, -3))
# S1 = Shape([triangle for triangle in toh() if triangle not in hexmaker(3,-3)+hexmaker(2,-2)])
# S1 = Shape([triangle for triangle in hexmaker(0,0)+[Triangle(1,1)] if triangle not in [Triangle(0,0)]])
# S1 = Shape(hexmaker(-1,1)+hexmaker(1,2)+hexmaker(2,1)+hexmaker(1,-1)+hexmaker(-1,-2))


""" edge data testing """
# S1 = HShape([Hexagon(0,0, [1, 1, 1, 0, -1, -1])])

"""4hex H2
takes too long"""

# priority = [
# Hexagon(-1, 1),
# Hexagon(1, 2),
# ]
#
# S1 = HShape([
# Hexagon(0, 0, [0, 0, 0, 1, -1, 0]),
# Hexagon(1, -1),
# Hexagon(2, 1),
# Hexagon(3, 0),
# ],
# priority = priority
# )

"""3hex H2
computes in 13 sec"""

# S1 = HShape(
# [Hexagon(0, 0, [0, 0, 0, -1, 0, -1]),
# Hexagon(2, 1, [0, 0, 1, 0, 0, 0]),
# Hexagon(1, -1)],
#
# )

""" 2-hexapillar
computes in 323 sec"""
S1 = HShape(
[Hexagon(0, 0, [1, 1, 0, -1, -1, 0]),
Hexagon(2, 1, [1, 1, -1, -1, -1, 0])],

)

# H1 = Hexagon(0, 0, [1, 0, 0, 0, 0, 0])
# H2 = Hexagon(1, 2, [0, 0, -1, 0, 0, 0])
# S1 = HShape([H1, H2])

# S1 = HShape([
# Hexagon(0, 0, [0, 0, 0, 0, -1, 0]),
# Hexagon(1, -1, [0, 0, 0, 0, 0, 1]),
# Hexagon(2, 1),
# Hexagon(3, 0),
# Hexagon(0, -3),
# ])

""" hexagon testing """
# S1 = HShape( [Hexagon(0,0), Hexagon(2,1), Hexagon(3,0)])
# S1 = HShape( [hex for hex in bhmaker(0,0) if hex not in [Hexagon(-2,-1), Hexagon(0,0)] ]  )
# S1 = HShape( bhmaker(0,0)+[Hexagon(-2,2), Hexagon(-2,-4), Hexagon(4,2), Hexagon(0,-3), Hexagon(3,0), Hexagon(4,-1)] )


""" This has types:
    1) Corona
    2) Boundary
    3) Base
"""
data_writer(S1, type = "heesch")
print("--- %s seconds ---" % (time.time() - start_time))
