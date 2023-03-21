import uuid
from pathlib import Path

from botocore.errorfactory import ClientError

from domain.entities.shared import UploadedFile


class S3Wrapper():
    def __init__(self, s3_client, bucket_name, bucket_location, key_prefix):
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.bucket_location = bucket_location
        self.key_prefix = key_prefix

    def upload_file(self, file):
        if not file:
            return None
        path = Path(file.filename)
        key = self.__generate_key(path.name)

        self.s3_client.upload_fileobj(file, self.bucket_name, key)
        return UploadedFile(key, path.name)

    def generate_link(self, key):
        if not key:
            return None
        s3_request_params = {"Bucket": self.bucket_name, "Key": key}
        return self.s3_client.generate_presigned_url(
            "get_object",
            Params=s3_request_params
        )

    def delete(self, key):
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=key
            )
        except ClientError:
            pass

    def is_exists(self, key):
        if not key:
            return False
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=key)
        except ClientError:
            return False
        return True

    def __generate_key(self, filename):
        return f"{self.key_prefix}{uuid.uuid4()}/{filename}"
