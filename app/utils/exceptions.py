class AppError(Exception):
    status_code = 500

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class BadRequestError(AppError):
    status_code = 400


class ValidationError(BadRequestError):
    pass


class NotFoundError(AppError):
    status_code = 404


class ConflictError(AppError):
    status_code = 409

