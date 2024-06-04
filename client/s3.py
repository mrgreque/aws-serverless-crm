import boto3
import os

class S3:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.session = boto3.Session(
            aws_access_key_id=os.environ.get('S3_ACCESS_KEY'),
            aws_secret_access_key=os.environ.get('S3_SECRET_ACCESS_KEY'),
            region_name='us-east-1'
        ).client('s3')

    def upload(self, data, key):
        # Upload data to S3 bucket
        success = self.session.put_object(Key=key, Body=data, Bucket=self.bucket_name)

    def read_file(self, key):
        # Read file from S3 bucket
        readed_file = self.session.get_object(Bucket=self.bucket_name, Key=key)
        try:
            data = readed_file["Body"].read().decode('utf-8')
            return data
        except Exception as e:
            raise e