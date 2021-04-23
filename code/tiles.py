from squareshapes import Square, Polyomino, bigsquare_maker

""" Tile 2 with H2"""
priority = [
Square(2,0),
Square(4,6),
]

T2H2 = Polyomino(
[
Square(0,0),
Square(0,2),
Square(0,4),
Square(0,6),
Square(-2,4),
Square(2,2),
Square(2,4),
Square(2,6),
Square(4,0),
Square(4,2),
Square(4,6),
],
priority = priority
)

""" My own tile """

my_own_tile = Polyomino(
[
Square( 0 , 6),
Square( 0 , 8),
Square( 0 , 10),
Square( 2 , 6),
Square( 2 , 8),
Square( 4 , 6),
Square( 4 , 8),
Square( 6 , 0),
Square( 6 , 2),
Square( 6 , 6),
Square( 6 , 8),
Square( 8 , 0),
Square( 8 , 2),
Square( 8 , 4),
Square( 8 , 6),
Square( 8 , 8),
Square( 8 , 10),
Square( 10 , 0),
# Square( 12 , 0), #optional square
],
priority = [
Square( 6, 4 )
]
)
