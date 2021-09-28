from Domain.UseCases.Account import StoreAccount
from Contracts import Controller, EmailValidator
from Core.Message import Message
from Presentation.Errors.ValidationError import ValidationError


class SignUpController(Controller):
    def __init__(self, email_validator: EmailValidator, store_account: StoreAccount):
        self.email_validator = email_validator
        self.store_account = store_account

    def handle(self, message: Message):
        required_fields = ['email', 'password', 'password_confirmation']

        for field in required_fields: 
            if not message.body.get(field):
                raise ValidationError({field: ['is required']})

        if message.body.get('password') != message.body.get('password_confirmation'):
            raise ValidationError({'password_confirmation': ['does not match with password']})

        valid_email = self.email_validator.is_valid(message.body.get('email'))
        if not valid_email:
            raise ValidationError({'email': ['is invalid']})

        account = self.store_account.store(message.body.get('email'), message.body.get('password'))
        return account
