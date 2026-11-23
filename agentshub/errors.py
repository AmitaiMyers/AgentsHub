"""Domain errors. Each interface maps these once to its own protocol."""


class DomainError(Exception):
    status_code = 400
    a2a_task_state = "TASK_STATE_REJECTED"

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ValidationFailed(DomainError):
    status_code = 400


class Unauthorized(DomainError):
    status_code = 401


class Forbidden(DomainError):
    status_code = 403


class NotFound(DomainError):
    status_code = 404


class Conflict(DomainError):
    status_code = 409


class QuotaExceeded(DomainError):
    status_code = 429
