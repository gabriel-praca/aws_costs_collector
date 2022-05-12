from abc import ABC, abstractmethod

class FetchABC(ABC):

    @abstractmethod
    def fetch(self) -> str:
        pass

    @abstractmethod
    def parse(self, obj) -> list:
        pass

    @abstractmethod
    def get_connection(self):
        pass
