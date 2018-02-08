""" Demonstrate determining extension from content type returned in response """
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import boto3

class S3BucketManager():
    def __init__(self, key=None, secret=None, boto_client=None, bucket_name=None):
        self._key = key
        self._secret = secret
        self._bucket_name = bucket_name
        self._boto_client=boto_client

        if self._bucket_name is None:
            self.bucket_name="/"

        if self._boto_client is None:
            self._boto_client = boto3.client('s3',
                                             aws_access_key_id=self._key,
                                             aws_secret_access_key=self._secret)

    def create(self):
        # create bucket, set
        self._boto_client.create_bucket(Bucket=self._bucket_name, ACL='public-read')

    def set_as_website(self):
        config = {
            'ErrorDocument': { 'Key': 'error.html' },
            'IndexDocument': { 'Suffix': 'index.html' },
        }

        self._boto_client.pub_bucket_website(
            Bucket=self._bucket_name,
            WebsiteConfiguration=config)
