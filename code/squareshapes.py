from math import sqrt
import numpy as np

class Square:
    """ This will make squares with the sides of length 2.
     It is built by specifying the origin."""

    def __init__(self, x, y):
        self.origin = np.array([x,y])
        self.verts = {
        "v1": (x-1, y-1),
        "v2": (x+1, y-1),
        "v3": (x+1, y+1),
        "v4": (x-1, y+1),
        }
        # we making the edges starting at the bottom, and then going counter-clockwise

        self.edges = [
        {"edge": {self.verts["v1"], self.verts["v2"]}, },
        {"edge": {self.verts["v2"], self.verts["v3"]}, },
        {"edge": {self.verts["v3"], self.verts["v4"]}, },
        {"edge": {self.verts["v4"], self.verts["v1"]}, },
        ]

    def plot_data(self):
        plottinglist = []
        for elem in self.edges:
            el = list(elem["edge"])
            xcoords = [ el[0][0], el[1][0] ]
            ycoords = [ el[0][1], el[1][1] ]
            print([xcoords,ycoords])
            plottinglist.extend([xcoords, ycoords, "b-"])
        return plottinglist


    # def to_data(self):
    #     return [self.origin[0], self.origin[1], self.edgedata]
    #
    # def __eq__(self, other):
    #     return (self.origin == other.origin and self.edgedata == other.edgedata)
    #
    # def flip(self):
    #
    #     def edgedata_flip(edgedata):
    #         new_edgedata = [
    #         edgedata[0],
    #         edgedata[5],
    #         edgedata[4],
    #         edgedata[3],
    #         edgedata[2],
    #         edgedata[1],
    #         ]
    #
    #         return new_edgedata
    #
    #     return Hexagon(-self.origin[0] + self.origin[1], self.origin[1], edgedata_flip(self.edgedata))
    #
    # def turn60(self):
    #
    #     def edgedata_turn60(edgedata):
    #         new_edgedata = [
    #         edgedata[5],
    #         edgedata[0],
    #         edgedata[1],
    #         edgedata[2],
    #         edgedata[3],
    #         edgedata[4],
    #         ]
    #         return new_edgedata
    #
    #     new_origin = (-self.origin[1]+self.origin[0], self.origin[0])
    #     return Hexagon(new_origin[0], new_origin[1], edgedata_turn60(self.edgedata))
    #
    # def translate(self, xval, yval):
    #     newx = self.origin[0] + xval
    #     newy = self.origin[1] + yval
    #     return Hexagon(newx, newy, edgedata = self.edgedata)

class Shape:
    """ These will be polyominoes"""

    def __init__(self, squares):
        self.squares = squares
