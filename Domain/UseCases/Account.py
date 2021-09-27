from abc import ABCMeta, abstractmethod
from Domain.Entities.Account import Account

class AddAccount(metaclass=ABCMeta):
  @abstractmethod
  def add(self, email: str, password: str) -> Account:
    pass
