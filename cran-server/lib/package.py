import tarfile
import re
import os

class Package:

    def __init__(self, fobj):
        self._fileobj = fobj
        self._tar = None
        self._description = None

    def _untar(self):
        return tarfile.open(fileobj=self._fileobj, mode="r:gz")

    def name(self):
        # TODO(troy.defreitas@uptake.com) Parse name of package from description file
        # e.g. _parse_name(self.description())
        return self._fileobj.filename

    def description(self):
        if not self._description and not self._tar:
            self._tar = self._untar()
            self._description = self._extract_desc(self._tar)
        return self._description


    @staticmethod
    def _extract_desc(tarf):
        for f in tarf.getmembers():
            if not re.search('DESCRIPTION', f.name) == None:
                return tarf.extractfile(f).read().decode('utf8')
        raise Exception('No Valid DESCRIPTION found')
