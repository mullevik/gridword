from enum import Enum
from typing import NamedTuple, List, Dict

import logging

logger = logging.getLogger(__name__)


class Direction(NamedTuple):
    x: int
    y: int


class PositionType(Enum):
    EMPTY = 0
    WALL = 1
    GOAL = 2
    DANGER = 3


class PositionData(NamedTuple):
    type: PositionType
    reward: float
    value: float = 0.


class Position(NamedTuple):
    x: int
    y: int


class Action(object):
    def __init__(self, name: str):
        self.name = name

    def execute(self, current_position: Position) -> Position:
        raise NotImplementedError


class UpAction(Action):

    def __init__(self):
        super().__init__("up")

    def execute(self, current_position) -> Position:
        return Position(x=current_position.x, y=current_position.y - 1)


class DownAction(Action):

    def __init__(self):
        super().__init__("down")

    def execute(self, current_position) -> Position:
        return Position(x=current_position.x, y=current_position.y + 1)


class LeftAction(Action):

    def __init__(self):
        super().__init__("left")

    def execute(self, current_position) -> Position:
        return Position(x=current_position.x - 1, y=current_position.y)


class RightAction(Action):

    def __init__(self):
        super().__init__("right")

    def execute(self, current_position) -> Position:
        return Position(x=current_position.x + 1, y=current_position.y)


class NoAction(Action):

    def __init__(self):
        super().__init__("nothing")

    def execute(self, current_position) -> Position:
        return current_position


class GridWorld(object):

    def __init__(self, path_to_map_file: str = "world_0.txt"):
        self.current_position: Position = None
        self.positions: Dict[Position, PositionData] = {}
        self._load_from_map_file(path_to_map_file)
        self.last_action = NoAction()

    def _load_from_map_file(self, path_to_map_file: str):
        # build grid world from map file
        with open(path_to_map_file) as file:
            lines = [line.rstrip('\n') for line in file]
            self.height = len(lines)
            for row, line in enumerate(lines):
                self.width = len(line)

                for column, char in enumerate(line):
                    new_position = Position(column, row)
                    if char == '-':
                        self.positions[new_position] = \
                            PositionData(type=PositionType.EMPTY, reward=0.)
                    elif char == 'S':
                        self.positions[new_position] = \
                            PositionData(type=PositionType.EMPTY, reward=0.)
                        self.current_position = new_position
                    elif char == 'W':
                        self.positions[new_position] = \
                            PositionData(type=PositionType.WALL, reward=0.)
                    elif char == 'G':
                        self.positions[new_position] = \
                            PositionData(type=PositionType.GOAL, reward=1.)
                    elif char == 'D':
                        self.positions[new_position] = \
                            PositionData(type=PositionType.DANGER, reward=-1.)
                    else:
                        raise ValueError("Unknown character ({}) in map {}"
                                         .format(char, path_to_map_file))

            if self.current_position is None:
                raise ValueError("No starting position detected in map {}"
                                 .format(path_to_map_file))

            logger.debug("Map file {} loaded ({} x {})"
                         .format(path_to_map_file, self.width, self.height))

    def does_contain(self, position) -> bool:
        if self.width > position.x >= 0 \
                and self.height > position.y >= 0:
            return True
        return False

    def is_wall(self, position: Position) -> bool:
        if self.positions[position].type == PositionType.WALL:
            return True
        return False

    def next_position(self, action: Action) -> Position:
        next_position = action.execute(self.current_position)

        if self.does_contain(next_position) \
                and not self.is_wall(next_position):
            return next_position
        return self.current_position

    def get_positions(self) -> Dict[Position, PositionData]:
        return self.positions

    def do_action(self, action: Action):
        self.last_action = action

    def update(self):
        self.current_position = self.next_position(self.last_action)
        self.last_action = NoAction()
