import pytest
from cranserver.lib.package import Package
from cranserver.lib.storage import FileStorage

@pytest.fixture
def fs():
    return FileStorage('.')


class TestFileStorage:

    def test_push_and_fetch(self, fs, pkg):
        fs.push(pkg)
        with fs.fetch('httr_1.3.1') as f:
            pkg = Package.from_tarball(f)
            assert pkg.name == 'httr'

    def test_contains(self, fs, pkg):
        assert pkg in fs
