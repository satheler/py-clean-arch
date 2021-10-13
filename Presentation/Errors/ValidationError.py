from typing import Dict, List
from Presentation.Errors.BaseError import BaseError


class ValidationError(BaseError):
    """Exception raised for errors in the user input validation.

    Attributes:
        errors -- validation errors
    """

    def __init__(self, errors: Dict[str, List[str]] = {}):
        self.errors = self.make_errors(errors)
        super().__init__('Validation fails')

    def make_errors(self, errors={}):
        """Returns a list of normalized errors"""
        MESSAGE = 0
        return [{field: value[MESSAGE]} for field, value in errors.items()]

    def to_dict(self):
        """Returns a dictionary of errors"""
        return {
            'message': self.__str__(),
            'errors': self.errors
        }
