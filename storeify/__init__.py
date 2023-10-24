"Data storage made simple!"
__version__ = "0.2.1"

from .errors import FileCreationError, OutOfSpace
from .base import Store, CDNStore
from .utils import generate_valid_key
from . import shared
from .memory import MemoryStore
from .file import FileStore
