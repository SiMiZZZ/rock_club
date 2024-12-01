from blacksheep.exceptions import HTTPException


class UserAlreadyExistsException(HTTPException):
    def __init__(self, message: str = "Пользователь с таким email уже зарегистрирован"):
        super().__init__(409, message)
