import os
import tempfile
import pathlib
import pytest
import requests
import sys

from cranserver.lib.package import Package

PKG_URL = "https://cran.r-project.org/src/contrib/httr_1.3.1.tar.gz"

@pytest.fixture(scope="session")
def cran_src_dir_empty():
    p = pathlib.Path(tempfile.mkdtemp())
    (p / 'src/contrib').mkdir(parents=True)
    os.chdir(p)

@pytest.fixture(scope="session")
def tarball_loc(cran_src_dir_empty):
    r = requests.get(PKG_URL, stream=True)
    filename = 'httr_1.3.1.tar.gz'
    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
    return filename

@pytest.fixture
def pkg(tarball_loc):
    with open(tarball_loc, 'rb') as f:
        yield Package(f)
