from blacksheep.exceptions import HTTPException


class UserAlreadyExistsException(HTTPException):
    def __init__(self, message: str = "Пользователь с таким email уже зарегистрирован"):
        super().__init__(409, message)


class InvalidAuthDataException(HTTPException):
    def __init__(self, message: str = "Пользователя с такими данными не существует"):
        super().__init__(400, message)


class InvalidUserDataException(HTTPException):
    def __init__(self, message: str = "Пользователя с таким id не существует"):
        super().__init__(400, message)


class BandDoesNotExistException(HTTPException):
    def __init__(self, message: str = "Группы с таким id не существует"):
        super().__init__(404, message)


class NoFileData(HTTPException):
    def __init__(self, message: str = "Файлы не переданы"):
        super().__init__(400, message)


class NotValidDateIntervalException(HTTPException):
    def __init__(self, message: str = "Введены некорректные параметры дат"):
        super().__init__(400, message)


class ReservedTimeRangeException(HTTPException):
    def __init__(self, message: str = "Данное время уже забронировано"):
        super().__init__(400, message)
