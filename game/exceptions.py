class PlayerException(Exception):
    pass


class CoordinatesOfBoardOutOfRangeException(PlayerException):
    pass


class InvalidValueOfFieldException(PlayerException):
    pass


class FieldIsNotEmptyException(PlayerException):
    pass


class IsNotYourMoveException(PlayerException):
    pass


class GameException(Exception):
    pass


class OnlyTwoPlayersInGameException(GameException):
    pass


class InvalidObjectPassed(GameException):
    pass


class ExitGameException(Exception):
    """Throw if you want to exit game"""
    pass
