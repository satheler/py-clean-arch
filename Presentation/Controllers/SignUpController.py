from Core.Message import Message
from Presentation.Errors.ValidationError import ValidationError


class SignUpController:
    def handle(self, message: Message):
        required_fields = ['name', 'email']

        for field in required_fields: 
            if not message.body.get(field):
                raise ValidationError({field: ['is required']})
