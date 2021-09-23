from Presentation.Errors.BaseError import BaseError


class BusinessError(BaseError):
    """Exception raised when a business rule is invalid.

    Attributes:
        title -- title of the business rule
        message -- explanation of the business rule
    """

    def __init__(self, title: str, message: str):
        self.title = title
        self.message = message

    def dict(self):
        """Returns the error as a dictionary"""
        return {
            'title': self.title,
            'message': self.message
        }
