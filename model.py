from enum import Enum
from typing import NamedTuple


class Direction(NamedTuple):
    x: float
    y: float


class Position(NamedTuple):
    x: float
    y: float


class Model(object):

    def __init__(self, initial_x: float, initial_y: float):
        self.direction = Direction(0., 0.)
        self.position = Position(initial_x, initial_y)

    def change_direction(self, new_direction: Direction):
        self.direction = new_direction

    def update(self):
        self.position = Position(self.position.x + self.direction.x,
                                 self.position.y + self.direction.y)
