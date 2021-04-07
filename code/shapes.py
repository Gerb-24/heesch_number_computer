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
        return Triangle(newx,newy, self.up)

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
        self.v3 = (self.x,self.y-1) if self.up else (self.x+1,self.y+1)
        self.up = not self.up
        self.edges = [{self.v1,self.v2},{self.v2, self.v3}, {self.v3, self.v1}]

    """ This takes in an edge and returns a Triangle that is next to the base triangle at that edge """
    def flip_around(self, edge):
        if self.up:
            if edge == {self.v1,self.v2}:
                return Triangle(0,0, up=False)
            elif edge == {self.v2,self.v3}:
                return Triangle(1,1, up=False)
            elif edge == {self.v1,self.v3}:
                return Triangle(0,1, up=False)
    def vertex_returner(self):
        return self.v1,self.v2,self.v3

    def turn30(self):
        #print(" a triangle has been turned")
        vertex_list = [self.v1, self.v2, self.v3]
        for i in range(len(vertex_list)):
            vertex_list[i] = (-vertex_list[i][1]+vertex_list[i][0], vertex_list[i][0])
        self.v1, self.v2, self.v3 = vertex_list[0], vertex_list[1], vertex_list[2]
        self.edges = [{self.v1,self.v2},{self.v2, self.v3}, {self.v3, self.v1}]
        print(vertex_list)


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

    def turn30(self):
        for triangle in self.triangles:
            triangle.turn30()
        self.edges = self.edgemaker(self.triangles)

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
        for elem in S1.outside():
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
