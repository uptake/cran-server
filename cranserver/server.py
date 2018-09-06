from __future__ import print_function
import os
import sys
import tarfile
import re
import json
from io import StringIO, BytesIO

from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import send_file
from flask import abort
from flask import render_template

import fasteners

from lib.package import Package
from lib.registry import Registry
from lib.registry import DuplicatePkgException

CONFLICT_CODE = 409
LOCK_CODE = 500

SRC_PACKAGES_FILE_LOC = 'src/contrib/PACKAGES'
LOCK_FILE_LOC = 'lockfile.lockfile'
LOCK_TIMEOUT = 5

DEFAULT_BUCKET = os.getenv('DEFAULT_BUCKET')
STORAGE_BACKEND = os.getenv('STORAGE_BACKEND', 'filesystem')

if STORAGE_BACKEND == 'filesystem':
    from lib.storage import FileStorage
    fsloc = os.getenv('CRANSERVER_FS_LOC', '/opt/cran')
    storage = FileStorage(fsloc)
elif STORAGE_BACKEND == 'aws' or STORAGE_BACKEND == 's3':
    from contrib.s3 import S3Storage
    storage = S3Storage()
else:
    raise "Storage backend '{}' not supported".format(STORAGE_BACKEND)

registry = Registry(storage)


app = Flask(__name__, template_folder='templates', static_folder='static')

# cran
# |- src
#   |- contrib
#      |- PACKAGES
#      |- PACKAGES.gz
#      |- * all tarballs
# |- bin
#   |- macosx
#     |- mavericks
#       |- contrib
#       |- {R-VERSION}
#         |- packages
#           |- <binaries>
#   |- windows


@app.route('/available', methods=['GET'])
def get_available():
    packages = (p.summary() for p in registry.values())
    pkg_dict = {}
    for p in packages:
        if not p:
            continue
        pkg_name = p.get('name')
        pkg_version = p.get('version')
        pkg_date = p.get('date')
        p['date'] = pkg_date.isoformat()  # convert date to string for JSON
        if pkg_dict.get(pkg_name) is not None:
            pkg_dict[pkg_name].append(p)
        else:
            pkg_dict[pkg_name] = [p]
    f = lambda x: x.get('date')
    results = list({'name': k, 'artifacts': sorted(v, key=f, reverse=True)}
                   for k, v in pkg_dict.items())
    return json.dumps(results)


@app.route('/', methods=['GET'])
def home_get():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def home_post():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']

    if file:
        a_lock = fasteners.InterProcessLock(LOCK_FILE_LOC)
        gotten = a_lock.acquire(
            blocking=True, delay=0.2, timeout=LOCK_TIMEOUT)
        try:
            if gotten:
                pkg = Package.from_tarball(file)
                file.seek(0)
                try:
                    registry.push(pkg)
                except DuplicatePkgException:
                    abort(CONFLICT_CODE, 'This package version already exists on the server.')
                return 'OK\n'
            else:
                print('Locking Error on Package Upload')
                abort(500, 'The server is busy, please try again')
        finally:
            if gotten:
                a_lock.release()

@app.route('/src/contrib/PACKAGES')
def packages_file():
    return registry.PACKAGES()

@app.route('/src/contrib/PACKAGES.<ext>')
def packages_file_rest(*args, **kwargs):
    abort(404)

@app.route('/src/<path:path>.tar.gz', methods=['GET'])
def packages(path):
    pkg_name = os.path.basename(path)
    pkg = registry.fetch(pkg_name)
    return send_file(BytesIO(pkg.fileobj), mimetype='application/octet-stream')


@app.route('/health')
def health():
    return '', 200
