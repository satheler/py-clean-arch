from abc import ABCMeta, abstractmethod


class EmailValidator(metaclass=ABCMeta):
    @abstractmethod
    def is_valid(self, email: str) -> bool:
        pass
