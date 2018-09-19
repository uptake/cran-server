import pytest

from cranserver.lib import FileStorage, InMemoryStorage

@pytest.fixture
def fs():
    return FileStorage('.')


class TestInMemoryStorage:

    def test_set(self, pkg):
        storage = InMemoryStorage()
        key = '/src/contrib/httr_1.3.1.tar.gz'
        storage[key] = pkg
        assert key in storage
