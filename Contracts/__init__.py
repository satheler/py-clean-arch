from abc import ABCMeta, abstractmethod

class Controller(metaclass=ABCMeta):
  @abstractmethod
  def handle(self, message):
    pass

class EmailValidator(metaclass=ABCMeta):
  @abstractmethod
  def is_valid(self, email: str) -> bool:
    pass
