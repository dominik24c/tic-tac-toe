from typing import Union

from .config import *


class Board:
    def __init__(self):
        self.__fields = []
        for i in range(SIZE_OF_BOARD):
            self.__fields.append([])
            for j in range(SIZE_OF_BOARD):
                self.__fields[i].append(None)

    def set_field(self, x: int, y: int, figure: str) -> None:
        self.__fields[x][y] = figure

    def get_fields(self) -> list[list[Union[None, M_O, M_X]]]:
        return self.__fields
