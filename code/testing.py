from hexshapes import Hexagon, HShape
import ast
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, Circle

import numpy as np

S1 = HShape([Hexagon(0,0, [1, 1, 1, 0, -1, -1])])
print(S1.heesch_computer())
