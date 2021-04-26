""" This file is just a library of different kinds of tiles """"

"""we first have the tiles with Heesch number 2 from Kaplans list """

""" Tile 1 with H2"""

tile1 = Polyomino(
[
Square(-2,4),
Square(0,0), Square(0,2), Square(0,4), Square(0,6),
Square(2,2), Square(2,4), Square(2,6),
Square(4,0), Square(4,2), Square(4,6),
],
priority = [
Square(2,0),
Square(4,6),
]

)

""" Tile 2 with H2 """
tile1 = Polyomino(
[
Square(0,2), Square(0,4),
Square(2,2),
Square(4,0), Square(4,2),
Square(6,2), Square(6,4), Square(6,6),
Square(8,4), Square(8,6),
Square(10,6),

],
priority = [
Square(2, 4),
Square(4, 4),
]


""" Tile 3 with H2 """
tile1 = Polyomino(
[
Square(0,2),
Square(2,2),
Square(4,2), Square(4,6), Square(4,8),
Square(6,0), Square(6,2), Square(6,4), Square(6,6), Square(6,8),
Square(8,8),

],
priority = [
Square(4, 6),
]
)

""" Tile 4 with H2"""

tile1 = Polyomino(
[
Square(0, 0), Square(0, 4),
Square(2, 0), Square(2, 2), Square(2, 4), Square(2, 6), Square(2, 8),
Square(4, 8),
Square(6, 6), Square(6, 8),
Square(8, 8),
],
priority = [
Square(4, 6),
]

)

""" Tile 5 with H2"""

tile1 = Polyomino(
[
Square(0, 2),
Square(2, 2),
Square(4, 2), Square(4, 4), Square(4, 6),
Square(6, 0), Square(6, 2), Square(6, 4), Square(6, 6),
Square(8, 2), Square(8, 4),
],
priority = [
]

)

""" Tile 6 with H2"""

tile1 = Polyomino(
[
Square(0, 4),
Square(2, 4),
Square(4, 0), Square(4, 2), Square(4, 4),
Square(6, 4), Square(6, 6),
Square(8, 2), Square(8, 4), Square(8, 6),
Square(10, 2),
],
priority = [
Square(6, 4), Square(6, 2),
]

)

""" Tile 10 with H2"""

tile1 = Polyomino(
[
Square(0, 4),
Square(2, 4),
Square(4, 2), Square(4, 4), Square(4, 8),
Square(6, 0), Square(6, 2), Square(6, 4), Square(6, 6), Square(6, 8),
Square(8, 6),
],
priority = [
Square(4, 6),
]

)

""" Now we get the tiles with Heesch number 3 """

""" The tower tile"""
tile1 = Polyomino(
[
Square(0, 2), Square(0, 4), Square(0, 6),
Square(2, 0), Square(2, 2), Square(2, 4),
Square(4, 2), Square(4, 4), Square(4, 6),
Square(6, 2), Square(6, 4), Square(6, 6),
Square(8, 0), Square(8, 2), Square(8, 4),
Square(10, 2), Square(10, 4), Square(10, 6),
Square(12, 2), Square(12, 4), Square(12, 6),
Square(14, 0), Square(14, 2), Square(14, 4),
Square(16, 2), Square(16, 4), Square(16, 6),
Square(18, 4), Square(18, 6),
],
priority = [
Square(2,6), Square(8,6), Square(14,6),
Square(4, 0), Square(6, 0),
Square(10, 0), Square(12, 0),
]
)


""" H3 tile """

tile1 = Polyomino(
[
Square( 0, 2), Square( 0, 4),
Square( 2, 0), Square( 2, 2), Square( 2, 4),
Square( 4, 0), Square( 4, 2), Square( 4, 4), Square( 4, 6),
Square( 6, 0), Square( 6, 2), Square( 6, 4), Square( 6, 6), Square( 6, 8),
Square( 8, 6), Square( 8, 8),
Square( 10, 8),

],
priority = []
)

# """ My own tile """
#
# my_own_tile = Polyomino(
# [
# Square( 0 , 6),
# Square( 0 , 8),
# Square( 0 , 10),
# Square( 2 , 6),
# Square( 2 , 8),
# # Square( 2 , 10),
# Square( 4 , 6),
# Square( 4 , 8),
# # Square( 4 , 10),
# Square( 6 , 0),
# Square( 6 , 2),
# Square( 6 , 6),
# Square( 6 , 8),
# # Square( 6 , 10),
# Square( 8 , 0),
# Square( 8 , 2),
# Square( 8 , 4),
# Square( 8 , 6),
# Square( 8 , 8),
# Square( 8 , 10),
# Square( 10 , 0),
# # Square( 12 , 0), #optional square
# ],
# priority = [
# Square( 6, 4 )
# ]
# )
