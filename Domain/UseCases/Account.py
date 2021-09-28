from abc import ABCMeta, abstractmethod
from Domain.Entities.Account import Account

class StoreAccount(metaclass=ABCMeta):
  @abstractmethod
  def store(self, email: str, password: str) -> Account:
    pass
