class CustomError(Exception):
    pass


class APIError(CustomError):
    pass


class OpenAIError(CustomError):
    pass


class LisumError(CustomError):
    pass
