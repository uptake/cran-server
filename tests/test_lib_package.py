#!/usr/bin/env python
import pathlib
import tempfile
import os

import pytest
import requests

from cranserver.lib.package import Package

PKG_URL = "https://cran.r-project.org/src/contrib/httr_1.3.1.tar.gz"
PKG_VERSION = "1.3.1"
PKG_DESCRIPTION = """Package: httr
Version: 1.3.1
Title: Tools for Working with URLs and HTTP
Description: Useful tools for working with HTTP organised by HTTP verbs
    (GET(), POST(), etc). Configuration functions make it easy to control
    additional request components (authenticate(), add_headers() and so on).
Authors@R: c(
    person("Hadley", "Wickham", , "hadley@rstudio.com", role = c("aut", "cre")),
    person("RStudio", role = "cph")
    )
Depends: R (>= 3.0.0)
Imports: jsonlite, mime, curl (>= 0.9.1), openssl (>= 0.8), R6
Suggests: httpuv, jpeg, knitr, png, testthat (>= 0.8.0), readr, xml2,
        rmarkdown, covr
VignetteBuilder: knitr
License: MIT + file LICENSE
RoxygenNote: 6.0.1
URL: https://github.com/r-lib/httr
BugReports: https://github.com/r-lib/httr/issues
NeedsCompilation: no
Packaged: 2017-08-18 17:47:58 UTC; hadley
Author: Hadley Wickham [aut, cre],
  RStudio [cph]
Maintainer: Hadley Wickham <hadley@rstudio.com>
Repository: CRAN
Date/Publication: 2017-08-20 14:44:14 UTC
"""


@pytest.fixture
def cran_src_dir_empty():
    p = pathlib.Path(tempfile.mkdtemp())
    (p / 'src/contrib').mkdir(parents=True)
    os.chdir(p)

@pytest.fixture
def tarball_loc(cran_src_dir_empty):
    r = requests.get(PKG_URL, stream=True)
    filename = 'httr_1.3.1.tar.gz'
    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
    return filename

@pytest.fixture
def pkg(tarball_loc):
    return Package('httr', open(tarball_loc, 'rb'))


class TestPackage:

    def test_description(self, pkg):
        desc = pkg.description()
        assert desc == PKG_DESCRIPTION

    def test_version(self, pkg):
        assert pkg.version == PKG_VERSION

    def test_id(self, pkg):
        assert pkg.id == 'httr_' + PKG_VERSION

    def test_from_tarball(self, tarball_loc):
        pkg = Package.from_tarball(open(tarball_loc, 'rb'))
        assert pkg.name == 'httr'
