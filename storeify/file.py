from .base import Store
from pathlib import Path


class FileStore(Store):
    _path: Path

    def __init__(self, directory: "str | Path"):
        self._path = Path(directory)
        self._path.mkdir(parents=True, exist_ok=True)

    def put(self, filename: str, data: bytes):
        path = self._generate_filepath(filename)
        path.write_bytes(data)

    def get(self, filename: str) -> bytes:
        path = self._generate_filepath(filename)
        return path.read_bytes()

    def delete(self, filename: str):
        path = self._generate_filepath(filename)
        path.unlink(missing_ok=True)

    def exists(self, filename: str) -> bool:
        path = self._generate_filepath(filename)
        return path.exists()

    def _generate_filepath(self, filename: str) -> Path:
        filename = encode(filename)
        return Path(self._path, filename)


def encode(filename: str) -> str:
    return filename
