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

    def __eq__(self, other):
        return np.array_equal(self.origin, other.origin)

    def plot_data(self):
        plottinglist = []
        for elem in self.edges:
            edge = list(elem["edge"])
            xcoords = [ edge[0][0], edge[1][0] ]
            ycoords = [ edge[0][1], edge[1][1] ]
            plottinglist.extend([xcoords, ycoords, "b-"])
        return plottinglist



    def translate(self, xval, yval):
        newx = self.origin[0] + xval
        newy = self.origin[1] + yval
        return Square(newx, newy)

    def rot_90(self):
         return Square(-self.origin[1], self.origin[0])

    def flip(self):
        return Square(-self.origin[0], self.origin[1])

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
    #     return squareagon(-self.origin[0] + self.origin[1], self.origin[1], edgedata_flip(self.edgedata))
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
    #     return squareagon(new_origin[0], new_origin[1], edgedata_turn60(self.edgedata))
    #
    # def translate(self, xval, yval):
    #     newx = self.origin[0] + xval
    #     newy = self.origin[1] + yval
    #     return squareagon(newx, newy, edgedata = self.edgedata)

class Polyomino:
    """ These will be polyominoes"""

    def __init__(self, squares, priority = []):
        def edgemaker():
            square_edge_list = [edge for square in self.squares for edge in square.edges]
            total_edge_list = [edge for edge in square_edge_list if square_edge_list.count(edge) == 1]
            return total_edge_list

        self.squares = squares
        self.edges = edgemaker()
        self.priority = priority

    def __eq__(self, other):
        xmin_s = min([square.origin[0] for square in self.squares])
        ymin_s = min([square.origin[1] for square in self.squares])
        xmin_o = min([square.origin[0] for square in other.squares])
        ymin_o = min([square.origin[1] for square in other.squares])
        for square in self.squares:
            if square not in other.translate(xmin_s-xmin_o,ymin_s-ymin_o).squares:
                return False
        return True

    def vertmaker(self):
        return [square.origin for square in self.squares]

    def translate(self, xval, yval):
        new_squares = []
        for square in self.squares:
            new_squares.append(square.translate(xval, yval))
        return Polyomino(new_squares)

    def translate_rel(self, square1, square2):
        return self.translate(square1.origin[0] - square2.origin[0], square1.origin[1] - square2.origin[1])

    def rot_90(self):
        new_squares = []
        for square in self.squares:
            new_squares.append(square.rot_90())
        return Polyomino(new_squares)

    def flip(self):
        new_squares = []
        for square in self.squares:
            new_squares.append(square.flip())
        return Polyomino(new_squares)


    def corona_maker(self, base_orientations, bookkeeping=False, heesch=False, printing=True):

        def not_occupied_in(elem, config, extra = False):
            config_squares = self.squares.copy() if extra else []

            for shape in config:
                config_squares.extend(shape.squares)
            for square in config_squares:
                if np.array_equal(elem.origin, square.origin):
                    return False

            return True

        # base_orientations_boundaries = [orientation.inside_remover() for orientation in base_orientations ]
        bookkeeper = []
        possible_config = []
        outside_list = self.outside()
        for i in range(len(outside_list)):
            if heesch:
                message = f" \r we are now at {int((i+1)/len(outside_list)*100)}% "
                print(message, end="")
            outs_square = outside_list[i]
            if len(possible_config) == 0:
                for index in range(len(base_orientations)):
                    for ns_square in base_orientations[index].squares:
                        new_shape = base_orientations[index].translate_rel(outs_square, ns_square)
                        if all(not_occupied_in(square, [self]) for square in new_shape.squares):
                            possible_config.append([new_shape])
                if bookkeeping:
                    bookkeeper.append(possible_config)
                if printing:
                    print(len(possible_config))

            else:
                new_possible_config = []
                for config in possible_config:
                    if not_occupied_in(outs_square, config):
                        for index in range(len(base_orientations)):
                            for ns_square in base_orientations[index].squares:
                                new_shape = base_orientations[index].translate_rel(outs_square, ns_square)
                                if all(not_occupied_in(square, config, extra=True) for square in new_shape.squares):
                                    new_config = config.copy()
                                    new_config.append(new_shape)
                                    new_possible_config.append(new_config)
                                else:
                                    continue
                    else:
                        #print(f" its occupied in the config? ")
                        new_possible_config.append(config)
                if new_possible_config == []:
                    return []
                possible_config = new_possible_config.copy()
                if bookkeeping:
                    bookkeeper.append(possible_config)
                if printing:
                    print(len(possible_config))
        return [[config] for config in possible_config] if heesch else possible_config


    def heesch_corona(self, coronalist):
        next_corona_list = []
        for i in range(len(coronalist)):
            corona_length = len(coronalist)
            message = f" \r we are now at {int((i)/corona_length*100)}% "
            print(message, end="")
            corona_config = coronalist[i]
            ns_squares = self.squares.copy()
            for corona in corona_config:
                for shape in corona:
                    ns_squares.extend(shape.squares)
            new_shape = Polyomino(ns_squares)
            new_corona = new_shape.corona_maker(self.orientations(), printing = False)

            for elem in new_corona:
                new_corona_config = corona_config.copy()
                new_corona_config.append(elem)
                next_corona_list.append(new_corona_config)
        return next_corona_list

    def heesch_computer(self):
        message = f"""
--------------------------------------
We are now computing the 1st corona
--------------------------------------
"""
        print(message)

        coronalist = self.corona_maker(self.orientations(), heesch=True, printing = False)
        if coronalist == []:
            print("")
            print("The heesch number is 0")
            return []
        else:
            i = 0
            while True:
                message = f"""
--------------------------------------
We are now computing the {i+2}nd corona
--------------------------------------
"""
                print(message)
                new_corona_list = self.heesch_corona(coronalist)
                if new_corona_list == []:
                    print("")
                    print(f" The heesch number is {i+1}")
                    return coronalist
                else:
                    coronalist = new_corona_list.copy()
                    i += 1

    def outside(self):
        def rawsquarees(squarelist):
            return [square(square.origin[0], square.origin[1]) for square in squarelist]

        bigsquarelist = []
        for vert in self.vertmaker():
            bigsquarelist.extend(bigsquare_maker(vert[0], vert[1]))
        res = self.priority.copy()
        for square in bigsquarelist:
            if square not in res:
                res.append(square)
        res = [square for square in res if square not in self.squares]
        return res

    def orientations(self):
        orientation_list =[
        self,
        self.rot_90(),
        self.rot_90().rot_90(),
        self.rot_90().rot_90().rot_90(),
        self.flip(),
        self.flip().rot_90(),
        self.flip().rot_90().rot_90(),
        self.flip().rot_90().rot_90().rot_90(),
        ]
        new_orientations_list = []
        for orientation in orientation_list:
            if orientation not in new_orientations_list:
                new_orientations_list.append(orientation)
        return new_orientations_list

    def plot_data(self):
        plottinglist = []
        for elem in self.edges:
            edge = list(elem["edge"])
            xcoords = [ edge[0][0], edge[1][0] ]
            ycoords = [ edge[0][1], edge[1][1] ]
            plottinglist.extend([xcoords, ycoords, "k-"])
        return plottinglist

def bigsquare_maker(x ,y):
    squares = [
    Square(x, y),
    Square(x, y-2),
    Square(x+2, y-2),
    Square(x+2, y),
    Square(x+2, y+2),
    Square(x, y+2),
    Square(x-2, y+2),
    Square(x-2, y),
    Square(x-2, y-2),
    ]
    return squares
