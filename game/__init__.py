from asyncio import AbstractEventLoop

from .board import Board
from .config import *
from .game import Game
from .player import Player


async def make_game(loop: AbstractEventLoop):
    board = Board()
    game = Game(board, loop)

    player1 = Player(M_O, game)
    player2 = Player(M_X, game)

    game.set_players(player1, player2)

    await game.run()
