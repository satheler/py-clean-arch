from Domain.Entities.Account import Account
from abc import ABCMeta, abstractmethod

class StoreAccountRepository(metaclass=ABCMeta):
  @abstractmethod
  def store(self, email: str, password: str) -> Account:
    pass
