

class UserNotFound(Exception):
    """Raised when a user is not found"""
    pass


class InvalidData(Exception):
    """Raised when request body doesn't match the required user schema"""
    pass


class UserExists(Exception):
    """Raised when a user with the same id already exists"""
    pass
