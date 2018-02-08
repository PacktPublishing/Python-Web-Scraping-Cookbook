""" Demonstrate determining extension from content type returned in response """
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from interface import implements
from core.i_blob_writer import IBlobWriter

import boto3

class S3BlobWriter(implements(IBlobWriter)):
    def __init__(self, bucket_name, boto_client=None):
        self._bucket_name = bucket_name

        if self._bucket_name is None:
            self.bucket_name = "/"

        # caller can specify a boto client (can reuse and save auth times)
        self._boto_client = boto_client

        # or create a boto client if user did not, use secrets from environment variables
        if self._boto_client is None:
            self._boto_client = boto3.client('s3')

    def write(self, filename, contents):
        # create bucket, and put the object
        self._boto_client.create_bucket(Bucket=self._bucket_name, ACL='public-read')
        self._boto_client.put_object(Bucket=self._bucket_name,
                                     Key=filename,
                                     Body=contents,
                                     ACL="public-read")
        print("Stored {0} in bucket {1}".format(filename, self._bucket_name))
