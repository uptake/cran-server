import os
import io
import boto3
import botocore
from lib.storage import Storage
from lib.package import Package


class S3Storage(Storage):

    def __init__(self, bucket_loc=None):
        s3 = boto3.resource('s3')
        self._bucket_loc = bucket_loc or os.getenv('DEFAULT_BUCKET')
        self.bucket = s3.Bucket(self._bucket_loc)

    def _objects(self, dir_prefix='dev'):
        prefix = dir_prefix + '/src/contrib/'
        return self.bucket.objects.filter(Prefix=prefix)

    def ls(self, dir_prefix='dev'):
        return [o.key for o in self._objects() if 'PACKAGES' not in o.key]

    def packages(self):
        return [self._s3obj_to_pkg_dict(obj) for obj in self._objects()]

    def _pkg_tupl(self, obj):
        return obj.key.split('/')[-1].replace('.tar.gz', '').split('_')

    def _s3obj_to_pkg_dict(self, obj):
        _name, _version = self._pkg_tupl(obj)

        return {
            'key': obj.key,
            'name': _name,
            'version': _version,
            'date': obj.last_modified.date(),
            'artifact_link': None
        }

    def fetch(self, pkg):
        target = io.StringIO()
        self.bucket.download_fileobj(pkg, target)
        return Package(target)

    def push(self, pkg):
        self.bucket.upload_fileobj(pkg._fileobj, pkg.name())


if __name__ == '__main__':
    s = S3Storage()

    for p in s.ls():
        print(p)

    for p in s.packages():
        print(p)
