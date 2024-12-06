from blacksheep.exceptions import HTTPException


class UserAlreadyExistsException(HTTPException):
    def __init__(self, message: str = "Пользователь с таким email уже зарегистрирован"):
        super().__init__(409, message)


class InvalidAuthDataException(HTTPException):
    def __init__(self, message: str = "Пользователя с такими данными не существует"):
        super().__init__(400, message)


class BandDoesNotExistException(HTTPException):
    def __init__(self, message: str = "Группы с таким id не существует"):
        super().__init__(404, message)
