from storeify import Store, MemoryStore, FileStore, RedisStore, S3StoreCDN
import pytest

stores = [
    MemoryStore(),
    FileStore("./data"),
]
get_class_name = lambda store: store.__class__.__name__

@pytest.mark.parametrize("store", stores, ids=get_class_name)
def test_put(store: Store):
    store.put("test.txt", b"hello world")
    assert store.exists("test.txt")
    assert store.get("test.txt") == b"hello world"


@pytest.mark.parametrize("store", stores, ids=get_class_name)
def test_delete(store: Store):
    store.put("test.txt", b"hello world")
    assert store.exists("test.txt")
    store.delete("test.txt")
    assert not store.exists("test.txt")
