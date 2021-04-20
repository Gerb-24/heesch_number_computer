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

    def to_data(self):
        data = {
        "x": self.origin[0],
        "y": self.origin[1],
        }
        return data

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

class FakePolyomino:
    def __init__(self, squares, shapecode = {"translation": (0, 0),"flipped": False,  "rotation": 0}):
        self.squares = squares
        self.shapecode = shapecode

    def rot_90(self):
        new_squares = []
        for square in self.squares:
            new_squares.append(square.rot_90())

        new_translation = (-self.shapecode["translation"][1],
        self.shapecode["translation"][0])

        new_flipped = self.shapecode["flipped"]
        new_rotation = (self.shapecode["rotation"]+90) % 360

        new_shapecode = {
        "translation": new_translation,
        "flipped": new_flipped,
        "rotation": new_rotation
        }

        return FakePolyomino(new_squares, shapecode = new_shapecode)


class Polyomino:
    """ These will be polyominoes"""

    def __init__(self, squares, priority = [], shapecode = {"translation": (0, 0),"flipped": False,  "rotation": 0}, collision_data = []):
        def edgemaker():
            square_edge_list = [edge for square in self.squares for edge in square.edges]
            total_edge_list = [edge for edge in square_edge_list if square_edge_list.count(edge) == 1]
            return total_edge_list

        self.squares = squares
        self.edges = edgemaker()
        self.priority = priority
        self.shapecode = shapecode
        if collision_data == []:
            print("no collision data")
        self.collision_data = self.collisions() if collision_data == [] else collision_data

    def __eq__(self, other):
        """ we assume here that there is the tile is not mirror symmetric or rotationtionally symmetric"""
        # translation_equal = np.array_equal(self.shapecode["translation"], other.shapecode["translation"])
        # flipped_equal = self.shapecode["flipped"] == other.shapecode["flipped"]
        # rotation_equal = self.shapecode["rotation"] == other.shapecode["rotation"]
        # shape_equal = translation_equal and flipped_equal and rotation_equal
        return self.shapecode == other.shapecode

    def to_data(self):
        data = {
        "squares": [square.to_data() for square in self.squares],
        "shapecode":self.shapecode,
        "priority": [square.to_data() for square in self.priority],
        "collision_data": self.collision_data
        }
        return data

    def orientations(self, fake = False):
        orientation_list =[
        self,
        self.rot_90(fake = fake),
        self.rot_90(fake = fake).rot_90(),
        self.rot_90(fake = fake).rot_90().rot_90(),
        self.flip(fake = fake),
        self.flip(fake = fake).rot_90(),
        self.flip(fake = fake).rot_90().rot_90(),
        self.flip(fake = fake).rot_90().rot_90().rot_90(),
        ]

        new_orientations_list = []
        for orientation in orientation_list:
            if orientation not in new_orientations_list:
                new_orientations_list.append(orientation)
        return new_orientations_list

    def collisions(self):
        collision_dict = {
        0: set(),
        1: set(),
        2: set(),
        3: set(),
        4: set(),
        5: set(),
        6: set(),
        7: set(),
        }

        key_dict = {
        "0F": 0,
        "90F": 1,
        "180F": 2,
        "270F": 3,
        "0T": 4,
        "90T": 5,
        "180T": 6,
        "270T": 7,
        }

        for orientation in self.orientations(fake = True):
            pre_key = f"""{orientation.shapecode["rotation"]}{"T" if orientation.shapecode["flipped"] else "F"}"""
            key = key_dict[pre_key]
            for or_square in orientation.squares:
                for base_square in self.squares:
                    coord = (
                    base_square.origin[0] - or_square.origin[0],
                    base_square.origin[1] - or_square.origin[1],
                    )
                    collision_dict[key].add(coord)
        return collision_dict

    def vertmaker(self):
        return [square.origin for square in self.squares]

    def translate(self, xval, yval):
        new_squares = []
        for square in self.squares:
            new_squares.append(square.translate(xval, yval))

        new_translation = (self.shapecode["translation"][0] + xval,
        self.shapecode["translation"][1] + yval)

        new_flipped = self.shapecode["flipped"]
        new_rotation = self.shapecode["rotation"]

        new_shapecode = {
        "translation": new_translation,
        "flipped": new_flipped,
        "rotation": new_rotation
        }

        new_collision_data = {}
        for bob in range(8):
            new_collision_data[bob] = {(coord[0] + xval, coord[1] + yval) for coord in self.collision_data[bob]}
        for elem in self.collision_data[1]:
            if (elem[0]+xval,elem[1]+yval) not in new_collision_data[1]:
                print(f"seomthing is fucked here")

        return Polyomino(new_squares, shapecode = new_shapecode, collision_data = new_collision_data)

    def translate_rel(self, square1, square2):
        return self.translate(square1.origin[0] - square2.origin[0], square1.origin[1] - square2.origin[1])

    def rot_90(self, fake = False):
        new_squares = []
        for square in self.squares:
            new_squares.append(square.rot_90())

        new_translation = (-self.shapecode["translation"][1],
        self.shapecode["translation"][0])

        new_flipped = self.shapecode["flipped"]
        new_rotation = (self.shapecode["rotation"]+90) % 360

        new_shapecode = {
        "translation": new_translation,
        "flipped": new_flipped,
        "rotation": new_rotation
        }

        if fake:
            return FakePolyomino(new_squares, shapecode = new_shapecode)
        else:
            new_collision_data = {}
            for i in range(8):
                if i < 4:
                    new_collision_data[i] = {(-coord[1], coord[0]) for coord in self.collision_data[ (i+3) % 4]}
                elif i <8:
                    new_collision_data[i] = {(-coord[1], coord[0]) for coord in self.collision_data[ ((i+3) % 4)+4]}

            return Polyomino(new_squares, shapecode = new_shapecode, collision_data = new_collision_data)

    def flip(self, fake = False):
        new_squares = []
        for square in self.squares:
            new_squares.append(square.flip())

        new_translation = (
        -self.shapecode["translation"][0],
        self.shapecode["translation"][1])

        new_flipped = not self.shapecode["flipped"]
        new_rotation = self.shapecode["rotation"]

        new_shapecode = {
        "translation": new_translation,
        "flipped": new_flipped,
        "rotation": new_rotation
        }

        if fake:
            return FakePolyomino(new_squares, shapecode = new_shapecode)
        else:
            new_collision_data = {
            0: {(-coord[0], coord[1]) for coord in self.collision_data[ 4 ] },
            1: {(-coord[0], coord[1]) for coord in self.collision_data[ 7 ] },
            2: {(-coord[0], coord[1]) for coord in self.collision_data[ 6 ] },
            3: {(-coord[0], coord[1]) for coord in self.collision_data[ 5 ] },
            4: {(-coord[0], coord[1]) for coord in self.collision_data[ 0 ] },
            5: {(-coord[0], coord[1]) for coord in self.collision_data[ 3 ] },
            6: {(-coord[0], coord[1]) for coord in self.collision_data[ 2 ] },
            7: {(-coord[0], coord[1]) for coord in self.collision_data[ 1 ] },
            }


            return Polyomino(new_squares, shapecode = new_shapecode, collision_data = new_collision_data)



        return Polyomino(new_squares, shapecode = new_shapecode)


    def corona_maker(self, base_orientations, heesch=False, printing=True):
        def config_collision(coord, config, key):
            if coord in self.collision_data[key]:
                return False
            for shape in config:
                if coord in shape.collision_data[key]:
                    return False
            return True
            # collision_dict = self.collision_data
            # for shape in config:
            #     for or_index in range(8):
            #         collision_dict[or_index].union(shape.collision_data[or_index])
            # return collision_dict

        def not_occupied_in(elem, config, extra = False):
            config_squares = self.squares.copy() if extra else []

            for shape in config:
                config_squares.extend(shape.squares)
            for square in config_squares:
                if np.array_equal(elem.origin, square.origin):
                    return False

            return True


        key_dict = {
        "0F": 0,
        "90F": 1,
        "180F": 2,
        "270F": 3,
        "0T": 4,
        "90T": 5,
        "180T": 6,
        "270T": 7,
        }

        possible_config = []
        outside_list = self.outside()
        for i in range(len(outside_list)):
            if heesch:
                message = f" \r we are now at {int((i+1)/len(outside_list)*100)}% "
                print(message, end="")
            outs_square = outside_list[i]
            if len(possible_config) == 0:
                for index in range(len(base_orientations)):
                    orientation = base_orientations[index]
                    pre_key = f"""{orientation.shapecode["rotation"]}{"T" if orientation.shapecode["flipped"] else "F"}"""
                    for ns_square in orientation.squares:
                        coord = (outs_square.origin[0]- ns_square.origin[0], outs_square.origin[1]- ns_square.origin[1])
                        if not coord in self.collisions()[key_dict[pre_key]]:
                            possible_config.append([orientation.translate(*coord)])
                if printing:
                    print(len(possible_config))

            else:
                new_possible_config = []
                for config in possible_config:
                    if not_occupied_in(outs_square, config):
                        for index in range(len(base_orientations)):
                            orientation = base_orientations[index]
                            pre_key = f"""{orientation.shapecode["rotation"]}{"T" if orientation.shapecode["flipped"] else "F"}"""
                            key = key_dict[pre_key]
                            for ns_square in orientation.squares:
                                coord = (outs_square.origin[0]- ns_square.origin[0], outs_square.origin[1]- ns_square.origin[1])
                                if config_collision(coord, config, key):
                                    new_config = config.copy()
                                    new_config.append(orientation.translate(*coord))
                                    new_possible_config.append(new_config)
                                else:
                                    continue
                    else:
                        new_possible_config.append(config)
                if new_possible_config == []:
                    return []
                possible_config = new_possible_config.copy()
                if printing:
                    print(len(possible_config))
        return [[config] for config in possible_config] if heesch else possible_config

    def outside(self):

        bigsquarelist = []
        for vert in self.vertmaker():
            bigsquarelist.extend(bigsquare_maker(vert[0], vert[1]))
        res = self.priority.copy()
        for square in bigsquarelist:
            if square not in res:
                res.append(square)
        res = [square for square in res if square not in self.squares]
        return res




#     def heesch_corona(self, coronalist):
#         next_corona_list = []
#         for i in range(len(coronalist)):
#             corona_length = len(coronalist)
#             message = f" \r we are now at {int((i)/corona_length*100)}% "
#             print(message, end="")
#             corona_config = coronalist[i]
#             ns_squares = self.squares.copy()
#             for corona in corona_config:
#                 for shape in corona:
#                     ns_squares.extend(shape.squares)
#             new_shape = FakePolyomino(ns_squares)
#             new_corona = new_shape.corona_maker(self.orientations(), printing = False)
#
#             for elem in new_corona:
#                 new_corona_config = corona_config.copy()
#                 new_corona_config.append(elem)
#                 next_corona_list.append(new_corona_config)
#         return next_corona_list
#
#     def heesch_computer(self):
#         message = f"""
# --------------------------------------
# We are now computing the 1st corona
# --------------------------------------
# """
#         print(message)
#
#         coronalist = self.corona_maker(self.orientations(), heesch=True, printing = False)
#         if coronalist == []:
#             print("")
#             print("The heesch number is 0")
#             return []
#         else:
#             i = 0
#             while True:
#                 message = f"""
# --------------------------------------
# We are now computing the {i+2}nd corona
# --------------------------------------
# """
#                 print(message)
#                 new_corona_list = self.heesch_corona(coronalist)
#                 if new_corona_list == []:
#                     print("")
#                     print(f" The heesch number is {i+1}")
#                     return coronalist
#                 else:
#                     coronalist = new_corona_list.copy()
#                     i += 1



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
