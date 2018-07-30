from __future__ import print_function
import os
import sys
import tarfile
import re
import json
from io import StringIO

from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import send_file
from flask import abort
from flask import render_template

import fasteners

from lib.package import Package

CONFLICT_CODE = 409
LOCK_CODE = 500

SRC_PACKAGES_FILE_LOC = 'src/contrib/PACKAGES'
LOCK_FILE_LOC = 'lockfile.lockfile'
LOCK_TIMEOUT = 5

DEFAULT_BUCKET = os.getenv('DEFAULT_BUCKET')
STORAGE_BACKEND = os.getenv('STORAGE_BACKEND', 'filesystem')

if STORAGE_BACKEND == 'filesystem':
    from lib.storage import FileStorage
    storage = FileStorage("/opt/cran/")
elif STORAGE_BACKEND == 'aws' or STORAGE_BACKEND == 's3':
    from contrib.s3 import S3Storage
    storage = S3Storage()
else:
    raise "Storage backend '{}' not supported".format(STORAGE_BACKEND)


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
    packages = storage.packages()
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


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']

        if file:
            a_lock = fasteners.InterProcessLock(LOCK_FILE_LOC)
            gotten = a_lock.acquire(
                blocking=True, delay=0.2, timeout=LOCK_TIMEOUT)
            try:
                if gotten:
                    file_loc = os.path.join('src/contrib', file.filename)
                    pkg = Package.from_tarball(file)
                    file.seek(0)
                    if pkg in storage:
                        abort(CONFLICT_CODE, 'This package version already exists on the server.')
                    storage.push(pkg)
                    return 'OK'
                else:
                    print('Locking Error on Package Upload')
                    abort(500, 'The server is busy, please try again')
            finally:
                if gotten:
                    a_lock.release()


@app.route('/src/<path:path>', methods=['GET'])
def packages(path):
    a_lock = fasteners.InterProcessLock(LOCK_FILE_LOC)
    gotten = a_lock.acquire(blocking=True, delay=0.2, timeout=LOCK_TIMEOUT)
    try:
        if gotten:
            pkg_name = os.path.basename(path)
            pkg_fobj = storage.fetch(pkg_name)
            with storage.fetch(pkg_name) as pkg_fobj:
                return send_file(pkg_fobj, mimetype='application/octet-stream')
        else:
            print('Locking Error on Package Upload')
            abort(LOCK_CODE, 'The server is busy, please try again')
    finally:
        if gotten:
            a_lock.release()


@app.route('/health')
def health():
    return '', 200
