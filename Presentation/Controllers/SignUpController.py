from Core.Message import Message
from Presentation.Errors.ValidationError import ValidationError


class SignUpController:
    def handle(self, message: Message):
        raise ValidationError({'name': 'is required'})
