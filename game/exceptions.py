class GameException(Exception):
    """Main game exception"""
    pass


class PlayerException(GameException):
    """Throw this exception, when player will make bad move"""
    pass


class CoordinatesOfBoardOutOfRangeException(PlayerException):
    pass


class InvalidValueOfFieldException(PlayerException):
    pass


class FieldIsNotEmptyException(PlayerException):
    pass


class IsNotYourMoveException(PlayerException):
    pass


class OnlyTwoPlayersInGameException(GameException):
    pass


class InvalidObjectPassed(GameException):
    pass


class GameOverException(GameException):
    """Throw if you want to exit game"""
    pass


class PlayerXIsWinnerException(GameOverException):
    pass


class PlayerOIsWinnerException(GameOverException):
    pass


class DrawException(GameOverException):
    pass
