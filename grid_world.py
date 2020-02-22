from enum import Enum
from typing import NamedTuple, List


class PositionType(Enum):
    EMPTY = 0
    WALL = 1


class Direction(NamedTuple):
    x: float
    y: float


class Position(NamedTuple):
    x: float
    y: float


class GridWorld(object):

    def __init__(self, initial_x: float, initial_y: float):
        self.direction = Direction(0., 0.)
        self.position = Position(initial_x, initial_y)

        self.map = [
            ["P", " ", " "],
            ["W", " ", " "],
            ["G", " ", "D"],
        ]

    def get_positions(self) -> List[Position]:
        return [
            Position(x=0, y=0),
            Position(x=1, y=0),
            Position(x=1, y=1),
        ]

    def change_direction(self, new_direction: Direction):
        self.direction = new_direction

    def update(self):
        new_position = Position(self.position.x + self.direction.x,
                                self.position.y + self.direction.y)

        if new_position in self.get_positions():
            self.position = new_position

