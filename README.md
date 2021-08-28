# heesch_machine
Frist cd into code, and run Python. Then enter:
```
from squareshapes import Square, Polyomino
from moretesting2 import main_func

```

make a tile, with for example

```
tile = Polyomino(
	[
		Square(2, 6),
		Square(4, 6),
		Square(6, 2), Square(6, 4), Square(6, 6),
		Square(8, 6), Square(8, 8),
		Square(10, 4), Square(10, 6), Square(10, 8),
		Square(12, 4),
	],
	priority = [
		Square(6,8),
		Square(12,6),
		Square(4,4),
		Square(8,4),
		Square(8,2),
		Square(10,2),
	]
)
```
to create the image for the surrounding tiles, enter:

```
main_func(tile)
```

To stop running the code when it is done, first close the image, and then enter
```
exit()
```
to close python.
