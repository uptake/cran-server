import pytest

from cranserver.lib.package import *
from cranserver.lib.registry import *

@pytest.fixture
def description(pkg_description):
    return Description(pkg_description)


class TestRegistry:

    def test_add(self, description):
        reg = Registry()
        reg.add(description)
        assert description.key() in reg
        # Test that you can't add duplicates
        with pytest.raises(DuplicatePkgException):
            reg.add(description)

    def test_packages(self, description):
        reg = Registry()
        reg.add(description)
        assert reg.PACKAGES() == description.dump()
