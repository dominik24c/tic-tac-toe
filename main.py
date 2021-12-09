import asyncio

from game import make_game

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(make_game(loop))
