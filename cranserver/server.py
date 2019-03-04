from __future__ import print_function
import os
from pathlib import Path
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

from cranserver.lib import Package
from cranserver.lib import Registry
from cranserver.lib import DuplicatePkgException

CONFLICT_CODE = 409
LOCK_CODE = 500

STORAGE_BACKEND = os.getenv('STORAGE_BACKEND', 'filesystem')

if STORAGE_BACKEND == 'filesystem':
    from cranserver.lib.storage import FileStorage
    fsloc = os.getenv('CRANSERVER_FS_LOC', '.')
    src_contrib_storage = FileStorage(Path(fsloc) / 'src/contrib')
elif STORAGE_BACKEND == 'memory':
    src_contrib_storage = InMemoryStorage()
elif STORAGE_BACKEND == 'aws' or STORAGE_BACKEND == 's3':
    DEFAULT_BUCKET = os.getenv('DEFAULT_BUCKET')
    from cranserver.contrib.s3 import S3Storage
    src_contrib_storage = S3Storage()
else:
    raise Exception(f'Storage backend "{STORAGE_BACKEND}" not supported')

src_contrib = Registry(src_contrib_storage)

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/available', methods=['GET'])
def get_available():
    packages = (p.summary() for p in src_contrib.values())
    pkg_dict = {}
    for p in packages:
        if not p:
            continue
        pkg_name = p.get('name')
        pkg_date = p.get('date')
        p['date'] = pkg_date.isoformat() if pkg_date else None
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
        pkg = Package.from_tarball(file)
        file.seek(0)
        try:
            src_contrib.push(pkg)
        except DuplicatePkgException:
            abort(CONFLICT_CODE, 'This package version already exists on the server.')
        return 'OK\n'
    return abort(400, 'You must upload a tarball file to use the POST endpoint.')

@app.route('/src/contrib/PACKAGES')
def packages_file():
    return src_contrib.PACKAGES()

@app.route('/src/contrib/PACKAGES.<ext>')
def packages_file_rest(*args, **kwargs):
    abort(404)

@app.route('/src/<path:path>.tar.gz', methods=['GET'])
def packages(path):
    pkg_key = os.path.basename(path)
    pkg = src_contrib.fetch(pkg_key)
    if not pkg:
        abort(404)
    return send_file(BytesIO(pkg.fileobj), mimetype='application/octet-stream')

@app.route('/health')
def health():
    return 'OK\n', 200


if __name__ == '__main__':
    app.run()
