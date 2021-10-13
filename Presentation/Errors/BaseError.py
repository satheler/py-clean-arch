class BaseError(Exception):
    """Base class for errors in this module."""

    def to_dict(self):
        """Returns the error as a dictionary"""
        return {
            'error': self.__class__.__name__,
            'message': self.message
        }
