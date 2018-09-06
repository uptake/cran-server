import os
import shutil
import time


class Storage(dict):
    """
    Storage is just a special dict.

    :key:   should be a string key
    :value: should be a stream of bytes
    """

    def PACKAGES(self):
        raise NotImplementedError


class InMemoryStorage(Storage):
    pass


class FileStorage(Storage):


    def __init__(self, directory):
        self.directory = directory

    def __iter__(self):
        return os.listdir(self.directory)

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

    def PACKAGES(self):
        return self.get('PACKAGES')
