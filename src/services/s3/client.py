import uuid
from enum import StrEnum

import boto3

from config import settings
from services.s3.types import File


class FileType(StrEnum):
    IMAGE = "image"


class S3Client:
    def __init__(
        self,
        aws_access_key: str = settings.S3_ACCESS_TOKEN,
        aws_secret_key: str = settings.S3_SECRET_KEY,
        bucket_name: str = settings.S3_BUCKET_NAME,
    ):
        self.s3 = boto3.resource(
            "s3",
            endpoint_url=settings.S3_ENDPOINT,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
        )
        self.bucket_name = bucket_name

    def upload_file(self, type: FileType, file: File):
        file_name = f"{type.value}/{uuid.uuid4()}{file.file_extension}"
        file_object = self.s3.Object(self.bucket_name, file_name)
        file_object.put(Body=file.data)
        return f"{settings.S3_DEFAULT_LINK}{file_name}"
