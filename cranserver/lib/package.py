import tarfile
import re
import os

class Package:

    def __init__(self, fileobj):
        self._fileobj = fileobj
        self._description = None

    def _untar(self):
        return tarfile.open(fileobj=self._fileobj, mode="r:gz")

    def description(self):
        if not self._description:
            self._description = self._extract_desc(self._untar())
            self._fileobj.seek(0)
        return self._description

    @property
    def fileobj(self):
        return self._fileobj

    @property
    def name(self):
        return self._attr_from_description('Package', self.description())

    @property
    def version(self):
        return self._attr_from_description('Version', self.description())

    @property
    def id(self):
        return self.name + '_' + self.version

    @property
    def filename(self):
        return self.id + '.tar.gz'

    @classmethod
    def from_tarball(cls, fileobj):
        return cls(fileobj)

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
