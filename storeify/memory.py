from .base import Store
from pathlib import Path


class MemoryStore(Store):
    _store: dict

    def __init__(self):
        self._store = {}

    def put(self, filename: str, data: bytes):
        self._store[filename] = data

    def get(self, filename: str) -> bytes:
        return self._store[filename]

    def delete(self, filename: str):
        del self._store[filename]

    def exists(self, filename: str) -> bool:
        return filename in self._store
