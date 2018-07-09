from abc import ABC, abstractmethod
import os
import time


class Storage(ABC):

    def __init__(self):
        "docstring"
        pass

    @abstractmethod
    def ls(self):
        "List all packages available."
        pass

    @abstractmethod
    def fetch(self, pkg):
        "Fetch package from storage backend."
        pass

    @abstractmethod
    def push(self, pkg):
        "Save package to storage backend."
        pass


class FileStorage(Storage):
    _PACKAGES = "src/contrib/PACKAGES"

    def __init__(self, directory):
        self.directory = directory

    # TODO(troy.defreitas@uptake.com) This should be part of the abstract base class
    def __contains__(self, pkg):
        return pkg.name() in self.ls()

    def _update_packages(self, pkg):
        with open(os.path.join(self.directory, self._PACKAGES), 'a') as f:
            f.write(pkg.description())

    def ls(self):
        files = os.listdir(os.path.join(self.directory, "src/contrib/"))
        return [f for f in files if 'PACKAGES' not in f]

    def packages(self):
        keys = self.ls()
        return [self._file_to_pkg_dict(k) for k in keys]

    def _pkg_tupl(self, key):
        return key.split('/')[-1].replace('.tar.gz', '').split('_')

    def _filepath(self, key):
        return os.path.join(self.directory, 'src/contrib', key)

    def _file_to_pkg_dict(self, f):
        _name, _version = self._pkg_tupl(f)
        last_modified = time.ctime(os.path.getmtime(self._filepath(f)))
        return {
            'key': f,
            'name': _name,
            'version': _version,
            'date': last_modified,
            'artifact_link': None
        }

    def fetch(self, pkg):
        fp = os.path.join(self.directory, "src/contrib/", pkg)
        return open(fp, 'rb')

    def push(self, pkg):
        # TODO(troy.defreitas@uptake.com) Implement rollback if either step fails
        fp = os.path.join(self.directory, "src/contrib/", pkg.name())
        with open(fp, 'wb') as f:
            pkg._fileobj.save(f)
        self._update_packages(pkg)
