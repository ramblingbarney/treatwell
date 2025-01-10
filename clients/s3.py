from os import environ
import boto3


from clients.base import BaseClient

bucket = environ.get("BUCKET")


class S3Client(BaseClient):
    def __init__(self):
        self._boto3_client = self._get_boto3_client()

    @staticmethod
    def _get_boto3_client():
        return boto3.client("s3")

    def get_object_by_filename(self, file_name_path: str) -> str:

        s3_object = self._boto3_client.get_object(Bucket=bucket, Key=file_name_path)
        return self._retrieve_body(s3_object=s3_object)

    def put_file_obj(self, file_obj: bytes, file_key: str) -> None:
        self._boto3_client.put_object(
            Body=file_obj,
            Bucket=bucket,
            Key=file_key,
        )

    def _retrieve_body(self, s3_object) -> str:
        return s3_object["Body"].read().decode("utf-8-sig")
