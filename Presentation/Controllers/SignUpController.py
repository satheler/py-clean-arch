from Contracts.Controller import Controller
from Core.Message import Message
from Presentation.Errors.ValidationError import ValidationError


class SignUpController(Controller):
    def handle(self, message: Message):
        required_fields = ['name', 'email', 'password', 'password_confirmation']

        for field in required_fields: 
            if not message.body.get(field):
                raise ValidationError({field: ['is required']})
