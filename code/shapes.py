class Triangle:

    """ Here we create triangles of side length 1"""

    def __init__(self, x, y, up = True):
        self.up = up
        self.x = x
        self.y = y
        self.v1, self.v2, self.v3 = ((self.x,self.y), (self.x+1,self.y), (self.x+1, self.y+1)) if self.up else ((self.x,self.y),(self.x+1,self.y),(self.x,self.y-1))
        self.verts = [self.v1, self.v2, self.v3]
        self.edges = [{self.v1,self.v2},{self.v2, self.v3}, {self.v3, self.v1}]

    def translate(self, xval, yval):
        newx = self.x + xval
        newy = self.y + yval
        return Triangle(newx,newy, up = self.up)

    def __str__(self):
        return f"{self.v1}, {self.v2}, {self.v3}"

    def __eq__(self, other):
        return(set(self.verts) == set(other.verts))

    def common_edge(self, other):
        for edge in self.edges:
            for other_edge in other.edges:
                if edge == other_edge:
                    return edge

    def flip(self):
        return Triangle(-self.v1[0]+self.v1[1],self.v1[1], up=self.up)


    def vertex_returner(self):
        return self.v1,self.v2,self.v3

    def turn60(self):
        #print(" a triangle has been turned")
        vertex_list = [self.v1, self.v2, self.v3]
        new_vertex_list = []
        for i in range(len(vertex_list)):
            new_vertex = (-vertex_list[i][1]+vertex_list[i][0], vertex_list[i][0])
            new_vertex_list.append(new_vertex)
        xmin = min([elem[0] for elem in vertex_list])
        xmax = max([elem[0] for elem in vertex_list])
        ymin = min([elem[1] for elem in vertex_list])
        ymax = max([elem[1] for elem in vertex_list])

        if (xmax, ymax) in vertex_list:
            return Triangle(xmin, ymin)
        else:
            return Triangle(xmin, ymax, up=False)

    def plot_data(self, color= "b-"):
        plottinglist = []
        for edge in self.edges:
            el = list(edge)
            xcoords = [el[0][0], el[1][0]]
            ycoords = [el[0][1]-el[0][0], el[1][1]-el[1][0]]
            plottinglist.extend([xcoords, ycoords, color])
        return plottinglist


class Shape:
    def __init__(self, triangles):
        self.triangles = triangles
        self.edges = self.edgemaker(self.triangles)
        self.verts = self.vertmaker(self.triangles)

    """ With these functions we instantiate some stuff"""
    def edgemaker(self, triangles):
        total_edge_list = triangles[0].edges
        edge_counter = []
        for i in range(len(triangles)-1):
            for edge in total_edge_list:
                for other_edge in triangles[i+1].edges:
                    if edge == other_edge:
                        edge_counter.append(edge)
            total_edge_list = total_edge_list + triangles[i+1].edges
            total_edge_list = [i for i in total_edge_list if i not in edge_counter]
            edge_counter = []
        return total_edge_list

    def vertmaker(self, triangles):
        vertex_list = []
        for triangle in triangles:
            vertex_list.extend(triangle.verts)
        vertex_list = list(set(vertex_list))
        # vertex_list = [elem for  elem in vertex_list if elem not in self.inside()]
        return vertex_list

    """ With these functions we edit the shape"""
    def translate(self, xval, yval):
        new_triangles = []
        for triangle in self.triangles:
            new_triangles.append(triangle.translate(xval, yval))
        return Shape(new_triangles)

    def translate_rel(self, tri1, tri2):
        return self.translate(tri1.v1[0]-tri2.v1[0], tri1.v1[1]-tri2.v1[1])

    def flip(self):
        new_triangles = []
        for triangle in self.triangles:
            new_triangles.append(triangle.flip())
        return Shape(new_triangles)

    def turn60(self):
        new_triangles = []
        for triangle in self.triangles:
            new_triangles.append(triangle.turn60())
        return Shape(new_triangles)

    def inside(self):
        vertex_list = []
        for triangle in self.triangles:
            if all(edge not in self.edges for edge in triangle.edges):
                vertex_list.extend(triangle.verts)
        vertex_list = list(set(vertex_list))
        return vertex_list

    def outside(self):
        hexlist = []
        for vert in self.verts:
            hexlist.extend(hexagon_maker(vert[0]-1,vert[1]))
        res = []
        for elem in hexlist:
            if elem not in res:
                res.append(elem)
        res = [elem for elem in res if elem not in self.triangles]
        return res

    def corona_maker(self, base_orientations):

        def not_occupied_in(elem, config):
            config_triangles = []
            for shape in config:
                config_triangles.extend(shape.triangles)
            return (elem not in config_triangles)

        bookkeeper = []
        possible_config = []
        outside_list = self.outside()
        #print(f"the outside list length is {len(outside_list)}")
        for elem in outside_list:
            if len(possible_config) == 0:
                for elem3 in [elem2 for elem2 in self.triangles if elem2.up == elem.up]:
                    #print(elem.up, elem3.up)
                    new_shape = self.translate_rel(elem, elem3)
                    if all(triangle not in self.triangles for triangle in new_shape.triangles):
                        possible_config.append([new_shape])
                bookkeeper.append(possible_config)

            else:
                new_possible_config = []
                for config in possible_config:
                    if not_occupied_in(elem, config):
                        for elem3 in [elem2 for elem2 in self.triangles if elem2.up == elem.up]:
                            new_shape = self.translate_rel(elem, elem3)
                            if all(triangle not in self.triangles and not_occupied_in(triangle, config) for triangle in new_shape.triangles):
                                new_config = config.copy()
                                new_config.append(new_shape)
                                new_possible_config.append(new_config)
                    else:
                        new_possible_config.append(config)

                possible_config = new_possible_config.copy()
                bookkeeper.append(possible_config)
        return possible_config

    """ With these function we output a list to be put into a plot
    as input we specify the color we want the line to have

    1) plot_data will give the edges of the shape
    2) outside_plot_data will give the edges of the surrounding triangles """
    def plot_data(self, color= "b-"):
        plottinglist = []
        for edge in self.edges:
            el = list(edge)
            xcoords = [el[0][0], el[1][0]]
            ycoords = [el[0][1]-el[0][0], el[1][1]-el[1][0]]
            plottinglist.extend([xcoords, ycoords, color])
        return plottinglist

    def outside_plot_data(self):
        plottinglist = []
        for elem in self.outside():
            for edge in elem.edges:
                el = list(edge)
                xcoords = [el[0][0], el[1][0]]
                ycoords = [el[0][1]-el[0][0], el[1][1]-el[1][0]]
                plottinglist.extend([xcoords, ycoords, "b-"])
        return plottinglist

def hexagon_maker(x,y):
    down_triangles = [Triangle(x,y, up=False), Triangle(x+1,y+1, up=False), Triangle(x+1,y, up=False)]
    up_triangles = [Triangle(x,y), Triangle(x,y-1), Triangle(x+1,y)]
    return down_triangles+up_triangles
