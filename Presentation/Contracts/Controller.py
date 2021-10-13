from abc import ABCMeta, abstractmethod


class Controller(metaclass=ABCMeta):
    @abstractmethod
    def handle(self, message):
        pass
