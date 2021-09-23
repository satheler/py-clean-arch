from Core.Message import Message
from Presentation.Errors.ValidationError import ValidationError


class SignUpController:
    def handle(self, message: Message):
        if not message.body.get('name'):
            raise ValidationError({'name': ['is required']})
        
        if not message.body.get('email'):
            raise ValidationError({'email': ['is required']})
        

