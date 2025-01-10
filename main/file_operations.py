import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path

from main.base import Base
from clients.s3 import S3Client

base_path_default = Path(__file__).parent


class FileOperations(Base):

    def __init__(self):
        self._s3_client = self._get_s3_client()

    @staticmethod
    def _get_s3_client() -> S3Client:
        return S3Client.get_client()

    def read_file_to_bytes(
        self,
        file_name: str,
        base_path=base_path_default,
    ) -> bytes:
        """Handle the process of reading file returning bytes"""
        file_path = (base_path / file_name).resolve()

        with open(file_path, "rb") as file:
            data = file.read()
            return data

    def write_to_file(
        self,
        data: list[str],
        file_name: str,
        base_path=base_path_default,
    ) -> None:
        """Handle the process of writing data to a file"""
        file_path = (base_path / file_name).resolve()

        df = pd.DataFrame(data)
        table = pa.Table.from_pandas(df)
        pq.write_table(table, file_path)

    def upload_to_cloud(self, file_object: bytes, file_key: str) -> None:
        self._s3_client.put_file_obj(file_obj=file_object, file_key=file_key)
