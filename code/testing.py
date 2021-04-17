from hexshapes2 import Hexagon, HShape
import ast
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, Circle

import numpy as np

S1 = HShape( [Hexagon(0,0), Hexagon(2,1), Hexagon(3,0)])

orientation_list = S1.orientations(equality = True)
print(orientation_list)
print(len(orientation_list))
