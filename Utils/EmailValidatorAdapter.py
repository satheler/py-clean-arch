from Contracts import EmailValidator

class EmailValidatorAdapter(EmailValidator):
  def is_valid(self, email: str) -> bool:
      return False
