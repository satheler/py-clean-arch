class Controller:
  def handle(self, message):
    raise NotImplementedError()

class EmailValidator:
  def is_valid(self, email: str):
    raise NotImplementedError()
