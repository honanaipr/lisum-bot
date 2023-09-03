class CustomError(Exception):
    pass


class APIError(CustomError):
    pass


class OpenAIError(CustomError):
    pass
