import pytest
from cranserver.lib.storage import *
from cranserver.lib.package import *

@pytest.fixture
def fs():
    return FileStorage('.')


class TestInMemoryStorage:

    def test_set(self, pkg):
        storage = InMemoryStorage()
        key = '/src/contrib/httr_1.3.1.tar.gz'
        storage[key] = pkg
        assert key in storage
