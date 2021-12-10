import asyncio
import random
from asyncio import AbstractEventLoop, Task
from itertools import chain
from typing import Union

from .board import Board
from .config import *
from .exceptions import OnlyTwoPlayersInGameException, InvalidObjectPassed, CoordinatesOfBoardOutOfRangeException, \
    InvalidValueOfFieldException, FieldIsNotEmptyException, PlayerException, IsNotYourMoveException, GameOverException, \
    DrawException, PlayerOIsWinnerException, PlayerXIsWinnerException
from .player import Player


class Game:
    def __init__(self, board: Board, loop: AbstractEventLoop):
        self.__board = board
        self.__players: list[Player] = []
        self.__players_tasks: list[Task] = []
        self.__loop = loop
        self.__stop = loop.create_future()
        self.__running = True
        self.__lock = asyncio.Lock()

    def set_players(self, *args) -> None:
        for arg in args:
            if isinstance(arg, Player):
                self.__players.append(arg)
            else:
                raise InvalidObjectPassed(f"Invalid argument passed! It must be instance of {self.__name__}")

        if len(self.__players) != 2:
            raise OnlyTwoPlayersInGameException()

    def draw_the_order_of_players(self) -> None:
        random.shuffle(self.__players)

    def next_player(self) -> Player:
        player = self.__players.pop(0)
        self.__players.append(player)
        print(player)
        return player

    async def _run_players(self) -> None:
        for player in self.__players:
            task = asyncio.ensure_future(player.listen())
            self.__players_tasks.append(task)

    async def _wait_for_players(self) -> None:
        print("CANCEL PLAYER players")
        for player in self.__players_tasks:
            player.cancel()

    def trigger_move_of_player(self) -> None:
        self.__players[1].unset_your_move()
        self.__players[0].set_your_move()

    async def run(self) -> None:
        self.draw_the_order_of_players()

        await self._run_players()
        self.trigger_move_of_player()

        while self.__running:
            print("in game")
            await asyncio.sleep(1)

        await self._wait_for_players()
        print("Exit game")
        # await self.__stop

    def _check_result_of_game_by_rows_or_columns(self, res: set, figure: Union[M_X, M_O]) -> None:
        if len(res) == 1 and figure in res:
            print(f'Winner is {figure}')
            if figure == M_X:
                raise PlayerXIsWinnerException()
            else:
                raise PlayerOIsWinnerException()

    def _is_end_of_game(self, figure_of_player: Union[M_X, M_O]) -> None:
        fields = self.__board.get_fields()

        for i in range(SIZE_OF_BOARD):
            # checking by rows
            self._check_result_of_game_by_rows_or_columns(set(fields[i]), figure_of_player)
            # checking by columns
            self._check_result_of_game_by_rows_or_columns({fields[0][i], fields[1][i], fields[2][i]}, figure_of_player)

        # checking by diagonally
        self._check_result_of_game_by_rows_or_columns({fields[0][0], fields[1][1], fields[2][2]}, figure_of_player)
        self._check_result_of_game_by_rows_or_columns({fields[0][2], fields[1][1], fields[2][0]}, figure_of_player)

        if None not in list(chain(*fields)):
            raise DrawException()

    async def legal_move(self, figure: str, id: str, x: int, y: int) -> None:
        async with self.__lock:
            try:
                print('in lock')
                if id != self.__players[0].get_id():
                    raise IsNotYourMoveException()
                elif not (0 <= x < SIZE_OF_BOARD and 0 <= y < SIZE_OF_BOARD):
                    raise CoordinatesOfBoardOutOfRangeException()
                elif figure not in (M_X, M_O):
                    raise InvalidValueOfFieldException()
                elif self.__board.get_fields()[x][y] is not None:
                    raise FieldIsNotEmptyException()
                self.__board.set_field(x, y, figure)
                self._is_end_of_game(figure)
                self.next_player()
                self.trigger_move_of_player()
                print('succeed')
            except GameOverException as e:
                self.__running = False
                print(f'{e.__class__.__name__.replace("Exception","")}')
                print("END GAME")
            except PlayerException as e:
                print(e.__class__.__name__)
                # print('error')
                pass
