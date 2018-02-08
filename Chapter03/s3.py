import requests
import botocore
import boto3

data = requests.get("http://localhost:8080/pages/planets.html").text

# create S3 client, use environment variables for keys
s3 = boto3.client('s3')

# the bucket
bucket_name = "planets-content"

# create bucket, set
s3.create_bucket(Bucket=bucket_name, ACL='public-read')
s3.put_object(Bucket=bucket_name, Key='planet.html',
              Body=data, ACL="public-read")
