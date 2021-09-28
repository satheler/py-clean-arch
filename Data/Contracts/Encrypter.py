from abc import ABCMeta, abstractmethod

class Encrypter(metaclass=ABCMeta):
  @abstractmethod
  def encrypt(self, value: str) -> str:
    pass
