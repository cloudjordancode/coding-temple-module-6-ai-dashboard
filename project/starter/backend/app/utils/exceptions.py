
# Exceptions

class AppException(Exception):
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


class NotFoundException(AppException):
    """Resource not found (404)."""
    def __init__(self, resource: str, resource_id):
        super().__init__(
            detail=f"{resource} with id {resource_id} not found",
            status_code=404
        )

class DuplicateTaskException(AppException):
    """Duplicate task (409)."""

    def __init__(self, detail: str = "Task already exists"):
        super().__init__(detail=detail, status_code=409)


class ForbiddenException(AppException):
    """Insufficient permissions (403)."""
    def __init__(self, detail: str = "You don't have permission"):
        super().__init__(detail=detail, status_code=403)