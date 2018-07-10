import tarfile
import re
import os

class Package:

    def __init__(self, name, fobj):
        # private
        self._fileobj = fobj
        self._tar = None
        self._description = None

        # public
        self.name = name

    def _untar(self):
        return tarfile.open(fileobj=self._fileobj, mode="r:gz")

    def description(self):
        if not self._description and not self._tar:
            self._tar = self._untar()
            self._description = self._extract_desc(self._tar)
        return self._description

    @property
    def version(self):
        return self._attr_from_description('Version', self.description())

    @property
    def id(self):
        return self.name + '_' + self.version

    @classmethod
    def from_tarball(cls, fileobj):
        desc = cls._extract_desc(tarfile.open(fileobj=fileobj, mode="r:gz"))
        name = cls._attr_from_description('Package', desc)
        return cls(name, fileobj)

    @staticmethod
    def _extract_desc(tarf):
        for f in tarf.getmembers():
            if not re.search('DESCRIPTION', f.name) == None:
                return tarf.extractfile(f).read().decode('utf8')
        raise Exception('No Valid DESCRIPTION found')

    @staticmethod
    def _attr_from_description(attr, description):
        for line in description.split('\n'):
            if (attr + ":") in line:
                return line.split(":")[1].strip()
