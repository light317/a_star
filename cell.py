from enum import Enum
import colors


class CellType(Enum):
    WALL = 1,
    ROAD = 2


class CellState(Enum):
    VISITED = 1,
    COMPUTED = 2,
    DONE = 3,
    UNTOUCHED = 4,
    PATH = 5,
    START = 6,
    END = 7


class Cell:
    def __init__(self, x: int, y: int, type: CellType):
        self.x = x
        self.y = y
        self.type = type
        self.state = CellState.UNTOUCHED
        self.h_score = 10000000
        self.g_score = 10000000
        self.f_score = 10000000
        self.came_from: Cell = None

    def __str__(self):
        came = "None"

        if self.came_from is not None:
            came = f'{self.came_from.x},{self.came_from.y} '
        return f'{self.x}, {self.y} -> {came}'

    def set_cell_type(self, type: CellType):
        self.type = type

    def get_h_score(self) -> int:
        return self.h_score + self.g_score

    def get_cell_color_by_state(self) -> (int, int, int):

        if self.type == CellType.WALL:
            return colors.black

        match self.state:
            case CellState.UNTOUCHED:
                return colors.white
            case CellState.VISITED:
                return colors.yellow
            case CellState.COMPUTED:
                return colors.blue
            case CellState.PATH:
                return colors.green
            case CellState.START:
                return colors.red
            case CellState.END:
                return colors.red
            case _:
                return colors.white

    def equals(self, b) -> bool:
        return self.x == b.x and self.y == b.y
