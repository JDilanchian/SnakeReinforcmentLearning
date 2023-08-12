from enum import Enum
from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])
BOX_SIZE = 20
SPEED = 1500
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
Direction = Enum('Direction', ['UP', 'LEFT', 'DOWN', 'RIGHT'], start = 0)
SNAKE_INITIAL = [Point(BOX_SIZE*3, BOX_SIZE), Point(BOX_SIZE*2, BOX_SIZE), Point(BOX_SIZE, BOX_SIZE)]

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
