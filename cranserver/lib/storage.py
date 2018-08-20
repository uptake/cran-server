from abc import ABC, abstractmethod
import os
import shutil
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

    def __init__(self, directory):
        self.directory = directory

    def __contains__(self, other):
        try:
            # if other is a cranserver.lib.package.Package
            return other.filename in self.ls()
        except AttributeError as e:
            # otherwise
            return other in self.ls()

    def PACKAGES(self):
        "Return PACKAGES file data."
        fp = os.path.join(self.directory, 'src/contrib/', 'PACKAGES')
        with open(fp, 'r') as f:
            return f.read()

    def packages(self):
        return [self._fp_to_pkg_dict(fp) for fp in self.ls()]

    def _pkg_tupl(self, fp):
        return fp.split('/')[-1].replace('.tar.gz', '').split('_')

    def _fp_to_pkg_dict(self, fp):
        _name, _version = self._pkg_tupl(fp)
        return {
            'key': fp,
            'name': _name,
            'version': _version,
            'date': None,
            'artifact_link': None
        }

    def ls(self):
        files = os.listdir(os.path.join(self.directory, 'src/contrib/'))
        return [f for f in files if 'PACKAGES' not in f]

    def _set(self, pkg_id, fobj):
        fp = os.path.join(self.directory, 'src/contrib/', pkg_id + '.tar.gz')
        with open(fp, 'wb') as f:
            shutil.copyfileobj(fobj, f, length=16384)

    def fetch(self, pkg_id):
        fp = os.path.join(self.directory, 'src/contrib/', pkg_id + '.tar.gz')
        return open(fp, 'rb')

    def push(self, pkg):
        return self._set(pkg.id, pkg.fileobj)
