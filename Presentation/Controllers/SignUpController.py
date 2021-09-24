from Contracts.Controller import Controller
from Contracts.EmailValidator import EmailValidator
from Core.Message import Message
from Presentation.Errors.ValidationError import ValidationError


class SignUpController(Controller):
    def __init__(self, email_validator: EmailValidator):
        self.email_validator = email_validator

    def handle(self, message: Message):
        required_fields = ['name', 'email', 'password', 'password_confirmation']

        for field in required_fields: 
            if not message.body.get(field):
                raise ValidationError({field: ['is required']})

        valid_email = self.email_validator.is_valid(message.body.get('email'))
        if not valid_email:
            raise ValidationError({'email': ['is invalid']})
