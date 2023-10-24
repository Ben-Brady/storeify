from .errors import FileCreationError, OutOfSpace
from io import BytesIO
from typing import Protocol
from random import randint
from abc import ABC, abstractmethod


class BasicStore(ABC):
    """
    A basic store that has no control over the allocation of keys
    """
    @abstractmethod
    def create(self, data: "bytes|BytesIO") -> str:
        """_description_

        Args:
            data (bytes|BytesIO): The data to store

        Raises:
            CreationError: Unable to create file
            OutOfSpace: Store is out of space

        Returns:
            str: The key of the created file
        """
        ...


    @abstractmethod
    def get(self, key: str) -> BytesIO:
        """Retrieve the data stored under a key

        Args:
            key (str): The key of the file to retrieve

        Raises:
            FileNotFoundError: The file does not exist

        Returns:
            BytesIO: The data stored under the key
        """
        ...


class Store(BasicStore):
    """
    A more advanced store that allows for more control over the data
    - Stores may encode keys, however they should be decoded when returned to the user
    """
    @abstractmethod
    def put(self, key: str, data: "bytes|BytesIO", *, upsert: bool = False):
        """_description_

        Args:
            key (str): The key to store the data under
            data (bytes|BytesIO): The buffer to store
            upsert (bool): Replace file if it already exists

        Raises:
            FileExistsError: if upsert is False and the file already exists
        """
        ...


    @abstractmethod
    def exists(self, key: str) -> bool:
        """Checks if an entry exists

        Args:
            key (str): _description_

        Raises:
            FileExistsError: if upsert is False and the file already exists

        Returns:
            bool: _description_
        """
        ...


    @abstractmethod
    def delete(self, key: str):
        """Deletes an entry using it's key
        If the file does not exist, this method should do nothing

        Args:
            key (str): The entry to delete
        """
        ...


    @abstractmethod
    def list(self) -> list[str]:
        """List all keys in the store

        Returns:
            list[str]: A list of keys
        """
        ...


class CDNStore(ABC):
    @abstractmethod
    def url(self, key: str) -> str:
        """Generates a publicly accessible URL for a file

        Args:
            key (str): The key of the file to generate a URL for

        Returns:
            str: The URL
        """
        ...
