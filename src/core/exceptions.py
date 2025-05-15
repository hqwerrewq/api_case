class AuthError(Exception):
    """Базовое исключение для ошибок аутентификации"""

class InvalidCredentialsError(AuthError):
    """Неправильные email/пароль"""

class UserInactiveError(AuthError):
    """Пользователь неактивен"""