import pytest
import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from main.file_operations import FileOperations
from clients.s3 import S3Client


class TestFileOperations:

    @pytest.fixture
    def file_operations_service(self) -> FileOperations:
        return FileOperations.get_class()

    def test_file_operations_service_instance(self, file_operations_service):
        assert isinstance(file_operations_service, FileOperations)

    def test_read_file_to_bytes(
        self,
        file_operations_service,
        test_file_movie_category,
        tmp_path,
    ):

        target_output = os.path.join(tmp_path, "animation.parquet")
        df = pd.DataFrame(test_file_movie_category)
        table = pa.Table.from_pandas(df)
        pq.write_table(table, target_output)

        result = file_operations_service.read_file_to_bytes(
            file_name="animation.parquet", base_path=tmp_path
        )

        assert result is not None

    def test_write_to_file(
        self, file_operations_service, test_file_movie_category, tmp_path
    ):

        file_operations_service.write_to_file(
            data=test_file_movie_category,
            file_name="animation.parquet",
            base_path=tmp_path,
        )

        file_read = file_operations_service.read_file_to_bytes(
            file_name="animation.parquet", base_path=tmp_path
        )

        assert type(file_read) is bytes

    def test_upload_to_cloud(
        self, mocker, file_operations_service, test_file_movie_category
    ):

        mock_put_file_obj = mocker.patch.object(S3Client, "put_file_obj")

        file_operations_service.upload_to_cloud(
            file_object=test_file_movie_category,
            file_key="animation.parquet",
        )

        mock_put_file_obj.assert_called_once()
