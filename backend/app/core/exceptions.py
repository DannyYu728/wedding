class NotFoundError(Exception):
    """Raised when a requested resource does not exist."""
    pass

class DuplicateError(Exception):
    """Raised when attempting to create a resource that already exists."""
    pass