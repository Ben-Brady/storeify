from random import randint
from abc import ABC, abstractmethod


class Store(ABC):
    @abstractmethod
    def put(self, key: str, data: bytes):
        ...

    @abstractmethod
    def get(self, key: str) -> bytes:
        """
        Raises:
            KeyError: If the key doesn't exist

        Args:
            key (str): The filename

        Returns:
            bytes: The file data
        """
        ...

    @abstractmethod
    def delete(self, key: str):
        ...

    def exists(self, key: str) -> bool:
        try:
            self.get(key)
        except KeyError:
            return False
        else:
            return True


class CDNStore(Store):
    @abstractmethod
    def url(self, filename: str) -> str:
        ...
