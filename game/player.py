from __future__ import annotations

import asyncio
import random
import uuid
from typing import Union, TYPE_CHECKING

from .config import *

if TYPE_CHECKING:
    from .game import Game


class Player:
    def __init__(self, figure: Union[M_X, M_O], game: Game):
        self.__figure = figure
        self.__game: Game = game
        self.__id = str(uuid.uuid4())

    def get_id(self) -> str:
        return self.__id

    def random_move(self) -> tuple[int, int]:
        x = random.randint(0, SIZE_OF_BOARD-1)
        y = random.randint(0, SIZE_OF_BOARD-1)
        # print(x, y)
        return x, y

    async def listen(self) -> None:
        try:
            while True:
                await self.__game.legal_move(self.__figure, self.__id, *self.random_move())
                await asyncio.sleep(1)
        except Exception as e:
            print(e)

    def __repr__(self):
        return f'{Player.__name__} - {self.__id}: {self.__figure}'