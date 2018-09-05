from io import StringIO, BytesIO

from .package import Package
from .package import Description


class DuplicatePkgException(Exception): pass


class Registry(dict):

    def __init__(self, storage=None):
        if storage:
            # On init, get the PACKAGES file
            pkgs = storage.PACKAGES()
            if pkgs:
                for description in Description.iter_paragraphs(pkgs):
                    self.add(description)

        self._storage = storage

    def add(self, description):
        key = description.name + '_' + description.version
        if key in self:
            raise DuplicatePkgException
        self[key] = description
        return key

    def push(self, pkg):
        # Extract the description from the package
        desc = pkg.description()

        # Write the package to the registry
        key = self.add(desc)

        # Push package binary data to storage
        self._storage[key] = pkg.fileobj

        # Push the new PACKAGES file to storage
        self._storage['PACKAGES'] = BytesIO(bytes(self.PACKAGES(), 'utf8'))

    def fetch(self, pkg_key):
        return Package.from_tarball(self._storage[pkg_key])

    def PACKAGES(self):
        return '\n'.join(v.dump() for _, v in self.items())
