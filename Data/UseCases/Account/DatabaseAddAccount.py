from Data.Contracts.Encrypter import Encrypter

class DatabaseAddAccount:
  def __init__(self, encrypter: Encrypter) -> None:
      self.encrypter = encrypter
  
  def add(self, email: str, password: str):
    self.encrypter.encrypt(password)