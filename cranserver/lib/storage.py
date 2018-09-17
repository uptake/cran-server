import os
import shutil
import time
from pathlib import Path
from collections.abc import MutableMapping


class Storage(MutableMapping):

    def PACKAGES(self):
        return self.get('PACKAGES')


class InMemoryStorage(dict, Storage):
    pass


class FileStorage(Storage):

    def __init__(self, directory):
        self.directory = directory

    def __iter__(self):
    # TODO When iterating, you shouldn't include the PACKAGES file
        return iter(os.listdir(self.directory))

    def __len__(self):
        return len(os.listdir(self.directory))

    def __getitem__(self, pkg_id):
        fp = os.path.join(self.directory, pkg_id + '.tar.gz')
        try:
            with open(fp, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            raise KeyError

    def __setitem__(self, pkg_id, fobj):
        fp = os.path.join(self.directory, pkg_id + '.tar.gz')
        with open(fp, 'wb') as f:
            shutil.copyfileobj(fobj, f, length=16384)

    def __delitem__(self, pkg_id):
        os.remove(Path(self.directory) / (pkg_id + 'tar.gz'))
