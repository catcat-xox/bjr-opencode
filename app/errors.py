class AppError(Exception):
    """Base class for domain errors that map to HTTP responses."""

    status_code = 400

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ValidationError(AppError):
    """Raised when request input does not satisfy validation rules."""

    status_code = 400


class NotFoundError(AppError):
    """Raised when a requested resource does not exist."""

    status_code = 404


class InsufficientStockError(AppError):
    """Raised when an item does not have enough available stock."""

    status_code = 400


class InvalidLoanStateError(AppError):
    """Raised when a loan cannot transition to the requested state."""

    status_code = 400
