import os
from pathlib import Path

import pytest
import requests

from cranserver.server import app
from cranserver.lib.package import Description

def fetch_package(pkg, version):
    r = requests.get(
        f'https://cran.r-project.org/src/contrib/{pkg}_{version}.tar.gz',
        stream=True)
    return r.raw

@pytest.fixture
def stringr():
    return fetch_package('stringr', version='1.3.1')

@pytest.fixture
def httr():
    return fetch_package('httr', version='1.3.1')

@pytest.fixture
def client():
    app.config['TESTING'] = True
    if not os.path.exists('src/contrib'):
        os.makedirs(Path('./src/contrib'))
    client = app.test_client()
    yield client

def test_get_PACKAGES_empty(client):
    resp = client.get('/src/contrib/PACKAGES')
    assert resp.data == b''  # assert empty because it's empty

def test_post_pkg(client, httr):
    resp = client.post('/', data={'file': (httr, 'httr_1.3.1.tar.gz')})
    assert resp.status_code == 200
    resp = client.get('/src/contrib/PACKAGES')
    assert resp.data != b''
    ls = list(Description.iter_paragraphs(resp.data))
    desc = ls[0]
    assert desc.name == 'httr'
    assert desc.version == '1.3.1'

def test_post_2nd_pkg(client, stringr):
    resp = client.post('/', data={'file': (stringr, 'stringr_1.3.1.tar.gz')})
    assert resp.status_code == 200
    resp = client.get('/src/contrib/PACKAGES')
    ls = list(Description.iter_paragraphs(resp.data))
    desc = ls[0]
    assert desc.name == 'httr'
    assert desc.version == '1.3.1'
    desc = ls[1]
    assert desc.name == 'stringr'
    assert desc.version == '1.3.1'

def test_get_pkg(client, stringr):
    resp = client.get('/src/contrib/stringr_1.3.1.tar.gz')
    assert resp.data == stringr.read()
    