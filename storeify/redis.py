from .base import Store
try:
    import redis
except ImportError:
    redis = None


class RedisStore(Store):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: "str|None" = None,
    ) -> None:
        if redis == None:
            raise ImportError(
                "Please install with redis support, pip install storeify[redis]"
            )

        self.redis = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            retry_on_timeout=True,
        )

    def put(self, filename: str, data: bytes):
        self.redis.set(filename, data)

    def exists(self, filename: str) -> bool:
        return self.redis.exists(filename) == 1

    def get(self, filename: str) -> bytes:
        data = self.redis.get(filename)
        if data is None:
            raise FileNotFoundError(filename)
        else:
            return data

    def delete(self, filename: str):
        self.redis.delete(filename)
