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
        new_rotation = (360 - self.shapecode["rotation"]) % 360

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


        def check_combinations(base_orientations, config):
            new_possible_config = []

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
            return new_possible_config


        possible_config = []
        outside_list = self.outside()
        for i in range(len(outside_list)):
            if heesch:
                message = f" \r we are now at {int((i+1)/len(outside_list)*100)}% "
                print(message, end="")
            outs_square = outside_list[i]
            if len(possible_config) == 0:
                possible_config.extend(check_combinations(base_orientations, []))
                if printing:
                    print(len(possible_config))

            else:
                new_possible_config = []
                for config in possible_config:
                    if not_occupied_in(outs_square, config):
                        new_possible_config.extend(check_combinations(base_orientations, config))
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

    def heesch_corona(self, possible_configs, coronalist, c_index):
        def sec_corona_maker(conf_corona_config):

            """
            We now translate, rotate and flip the whole config so that the start_tile
            is the same as the base tile.
            """

            def transform(st_tile, configuration):

                def flip(flipped, tile):

                    """ A function that flips a tile if flipping is true,
                    otherwise it just returns the tile """

                    if flipped:
                        return tile.flip()
                    else:
                        return tile

                def rotate(rotation, tile):

                    """ A function that can rotate a tile
                    by 90 degrees multiple times"""

                    if rotation == 0:
                        return tile
                    else:
                        return rotate(rotation - 90, tile.rot_90())

                def translate(translation, tile):

                    """ A function that translates a tile
                    just to keep things more organised """

                    return tile.translate(*translation)

                sc = st_tile.shapecode
                translation = ( -sc["translation"][0], -sc["translation"][1])
                flipped = sc["flipped"]
                rotation = 360 - sc["rotation"]

                transformed_config = [flip(flipped, rotate(rotation, translate(translation, tile))) for tile in configuration]

                return transformed_config

            """
            Now we take a for loop over all the coronas in possible_configs
            When this corona fits we append it to the list of the new possible configurations
            A corona fits if all of the tiles that do collide with fixed configuration
            are actually part of that configuration.
            """

            def collides_with(tile, configuration):

                """ In here we check if a tile collides with one of the tiles in a configuration """

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

                coord = tile.shapecode["translation"]
                pre_key = f"""{tile.shapecode["rotation"]}{"T" if tile.shapecode["flipped"] else "F"}"""
                key = key_dict[pre_key]

                for conf_tile in configuration:
                    if coord in conf_tile.collision_data[key]:
                        return True
                return False

            def retransform(st_tile, corona):

                def flip(flipped, tile):

                    """ A function that flips a tile if flipping is true,
                    otherwise it just returns the tile """

                    if flipped:
                        return tile.flip()
                    else:
                        return tile

                def rotate(rotation, tile):

                    """ A function that can rotate a tile
                    by 90 degrees multiple times"""

                    if rotation == 0:
                        return tile
                    else:
                        return rotate(rotation - 90, tile.rot_90())

                def translate(translation, tile):

                    """ A function that translates a tile
                    just to keep things more organised """

                    return tile.translate(*translation)

                sc = st_tile.shapecode
                translation = sc["translation"]
                flipped = sc["flipped"]
                rotation = sc["rotation"]

                retransformed_corona = [translate(translation, rotate(rotation, flip(flipped, tile))) for tile in corona]

                return retransformed_corona

            """
            new_c_configs now contains the all the possible coronas
            around the start_tile that fit with the fixed configuration.
            """

            """
            In the same way as we did with the corona_maker function
            we now want to combine these with the old config to get a list of possible_c_configs
            for every tile in the corona of the config we will now change
            the possible_c_configs to be all of the currently possible_c_configs
            """

            # config = [self] + conf_corona
            conf_corona = conf_corona_config[c_index]
            pre_possible_c_configs = conf_corona_config.copy()
            pre_possible_c_configs.append([])
            possible_c_configs = [ pre_possible_c_configs ]

            """
            So here we loop over the tiles in the corona of the config
            where we start at tile 1, since we already have done tile 0
            """
            #print(f"the length of conf_corona: {len(conf_corona)}")
            for start_num in range(len(conf_corona)):
                print(f" we our now at tile {start_num+1} out of {len(conf_corona)}")
                start_tile = conf_corona[start_num]

                """ We now go in a loop over all the c_configs in possible_c_configs """
                new_possible_c_configs = []
                for c_config in possible_c_configs:
                    """
                    Since we now want to work with c_config with corona structure
                    we need to define something new that we want to translate
                    which we call the absolute c config
                    """
                    # print(c_config[1])
                    abs_c_config = [self]
                    for abs_index in range(c_index+1):
                        abs_c_config.extend(c_config[abs_index])
                    transformed_abs_c_config = transform(start_tile, abs_c_config)

                    """
                    For this recentered absoltue c_config we will append all of the
                    retransformed corona that fit with the transformed c_config
                    """

                    new_c_configs = []
                    for corona in coronalist:
                        if all(c_tile in transformed_abs_c_config for c_tile in corona if collides_with(c_tile, transformed_abs_c_config)):
                            retransformed_corona = [ tile for tile in retransform( start_tile, corona ) if tile not in abs_c_config ]
                            # new_c_configs.append( c_config + retransformed_corona )
                            """
                            We first copy the current c_config in corona structure
                            and add the new retransformed_corona to it
                            then we append this to new_c_configs, this then contains all the new_possible_c_configs at the end
                            """
                            c_config_with_added_corona = c_config.copy()
                            c_config_with_added_corona[c_index+1] = c_config_with_added_corona[c_index+1] + retransformed_corona
                            new_c_configs.append( c_config_with_added_corona )

                    new_possible_c_configs.extend( new_c_configs )

                """
                If we no corona fits anymore for every possible c_config,
                then the original config is dead
                """

                if new_possible_c_configs == []:
                    possible_c_configs = []
                    break

                possible_c_configs = new_possible_c_configs.copy()

            return possible_c_configs

        second_configs = []
        for conf_corona_index in range(len(possible_configs)):
            print( f" We are at corona {conf_corona_index} out of {len(possible_configs)}  " )
            """
            the conf_corona is the last corona in the possible_config,
            """
            conf_corona_config = possible_configs[conf_corona_index]


            second_configs.extend(sec_corona_maker(conf_corona_config))
        print(f"in total there are {len(second_configs)} working configurations")

        return second_configs

    def heesch_computer(self):
        def has_holes(config, output = False ):
            total_squares = set()
            for shape in config+[tile1]:
                total_squares = total_squares.union({(square.origin[0],square.origin[1]) for square in shape.squares})
            extended_squares = set()
            for square in total_squares:
                extended_squares = extended_squares.union({
                square,
                (square[0], square[1]-2),
                (square[0]+2, square[1]-2),
                (square[0]+2, square[1]),
                (square[0]+2, square[1]+2),
                (square[0], square[1]+2),
                (square[0]-2, square[1]+2),
                (square[0]-2, square[1]),
                (square[0]-2, square[1]-2),
                })
            without_inside = extended_squares.difference(total_squares)

            # getting a starting position
            xmin = min({coord[0] for coord in without_inside})
            ymin = min({coord[1] for coord in without_inside if coord[0] == xmin})
            mincoord = (xmin, ymin)

            # computing the connected component and removing them
            coords = { mincoord }
            while coords != set():
                without_inside = without_inside.difference(coords)
                new_coords = set()
                for coord in coords:
                    nextcoords = {
                    (coord[0], coord[1]-2),
                    (coord[0]+2, coord[1]),
                    (coord[0], coord[1]+2),
                    (coord[0]-2, coord[1]),
                    }
                    nextcoords = {n_coord for n_coord in nextcoords if n_coord in without_inside}
                    new_coords = new_coords.union(nextcoords)
                coords = new_coords

            return without_inside if output else (without_inside != set())

        coronalist = self.corona_maker(self.orientations(), heesch=True)

        if coronalist == []:
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
                new_corona_list = self.heesch_corona(coronalist, i)
                if new_corona_list == []:
                    print(f" The heesch number is {i+1}")
                    return coronalist
                else:
                    coronalist = new_corona_list.copy()
                    i += 1


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
