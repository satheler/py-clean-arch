from Domain.UseCases.Account import StoreAccount
from Presentation.Adapters.Message import Message
from Presentation.Contracts.Controller import Controller
from Presentation.Errors.ValidationError import ValidationError
from Validators.Contracts.EmailValidator import EmailValidator


class SignUpController(Controller):
    def __init__(self, email_validator: EmailValidator, store_account: StoreAccount):
        self.email_validator = email_validator
        self.store_account = store_account

    def handle(self, message: Message):
        required_fields = ['email', 'password', 'password_confirmation']

        for field in required_fields:
            if not message.content.get(field):
                raise ValidationError({field: ['is required']})

        if message.content.get('password') != message.content.get('password_confirmation'):
            raise ValidationError(
                {'password_confirmation': ['does not match with password']})

        valid_email = self.email_validator.is_valid(
            message.content.get('email'))
        if not valid_email:
            raise ValidationError({'email': ['is invalid']})

        account = self.store_account.store(
            email=message.content.get('email'),
            password=message.content.get('password')
        )
        return account
