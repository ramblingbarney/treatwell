from os import environ
import pytest

from clients.s3 import S3Client


class TestS3Client:
    @pytest.fixture
    def mock_boto3_client(self, mocker):
        return mocker.patch.object(S3Client, "_get_boto3_client")

    @pytest.fixture
    def s3_client(self):
        return S3Client.get_client()

    @pytest.fixture
    def bucket_name(self):
        return environ.get("BUCKET")

    def test_get_client_instance(self, mock_boto3_client, s3_client):
        assert isinstance(s3_client, S3Client)
        mock_boto3_client.assert_called_once()

    def test_upload_file_obj(self, mock_boto3_client, s3_client, bucket_name):
        test_file_obj = b"test-file-obj"
        test_file_key = "test-file-key"
        result = s3_client.put_file_obj(file_obj=test_file_obj, file_key=test_file_key)

        assert result is None
        mock_boto3_client.return_value.put_object.assert_called_once_with(
            Body=test_file_obj, Bucket=bucket_name, Key=test_file_key
        )

    def test_retrieve_body(self, mocker, mock_boto3_client, s3_client):
        client = s3_client
        mocked_s3_object = mocker.MagicMock()
        mocked_s3_object.read.return_value.decode.return_value = b"test-string"

        result = client._retrieve_body(s3_object={"Body": mocked_s3_object})

        assert result == mocked_s3_object.read.return_value.decode.return_value
        mock_boto3_client.assert_called_once()
        mocked_s3_object.read.assert_called_once()
        mocked_s3_object.read.return_value.decode.assert_called_with("utf-8-sig")

    def test_get_object_by_filename(
        self, mocker, mock_boto3_client, s3_client, bucket_name
    ):
        client = s3_client
        filename = "test-filename"
        mocked_retrieve_body = mocker.patch.object(S3Client, "_retrieve_body")
        mocked_get_object = mocker.MagicMock()
        mock_boto3_client.return_value.get_object.return_value = mocked_get_object

        result = client.get_object_by_filename(file_name_path=filename)
        mock_boto3_client.return_value.get_object.assert_called_with(
            Bucket=bucket_name, Key=filename
        )
        mocked_retrieve_body.assert_called_once_with(s3_object=mocked_get_object)
        assert result == mocked_retrieve_body.return_value
