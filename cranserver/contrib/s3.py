import os
import io
from contextlib import contextmanager

import boto3
import botocore
from lib.storage import Storage
from lib.package import Package


class S3Storage(Storage):

    def __init__(self, bucket_loc=None):
        s3 = boto3.resource('s3')
        self._bucket_loc = bucket_loc or os.getenv('DEFAULT_BUCKET')
        self.bucket = s3.Bucket(self._bucket_loc)
        
    def __iter__(self):
        prefix = '/src/contrib'
        objs = self.bucket.objects.filter(Prefix=prefix)
        for el in objs:
            yield el.key

    def __len__(self):
        return len(list(self.__iter__()))

    def __getitem__(self, pkg_id):
        target = io.StringIO()
        self.bucket.download_fileobj(pkg_id, target)
        return target

    def __setitem__(self, pkg_id, fobj):
        self.bucket.upload_fileobj(fobj, pkg_id)
    
    def __delitem__(self, pkg_id):
        pass


if __name__ == '__main__':
    s = S3Storage()

    for p in s:
        print(p)
