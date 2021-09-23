from typing import Dict, List
from Presentation.Errors.BaseError import BaseError


class ValidationError(BaseError):
    """Exception raised for errors in the user input validation.

    Attributes:
        errors -- validation errors
    """

    def __init__(self, errors: Dict[str, List[str]] = {}):
        self.message = 'Validation fails'
        self.errors = self.make_errors(errors)

    def make_errors(self, errors={}):
        """Returns a list of normalized errors"""
        MESSAGE = 0
        return [{field: value[MESSAGE]} for field, value in errors.items()]
