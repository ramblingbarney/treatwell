import pytest

from app import app as create_app
from clients.async_base_api import AsyncBaseApi
from main.file_operations import FileOperations


import asyncio
from typing import Callable, TypeVar


from werkzeug import Response
from flask.testing import FlaskClient


T = TypeVar("T")


async def call(f: Callable[[], T]) -> T:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor=None, func=f)


class AsyncTestClient(FlaskClient):
    """A facade for the flask test client."""

    async def get(self, *args, **kwargs) -> Response:
        parent = super()
        return await call(lambda: parent.get(*args, **kwargs))

    async def post(self, *args, **kwargs) -> Response:
        parent = super()
        return await call(lambda: parent.post(*args, **kwargs))

    async def delete(self, *args, **kwargs) -> Response:
        parent = super()
        return await call(lambda: parent.delete(*args, **kwargs))

    async def put(self, *args, **kwargs) -> Response:
        parent = super()
        return await call(lambda: parent.put(*args, **kwargs))


class TestApp:

    @pytest.fixture()
    def app(self):
        app = create_app
        app.config.update({"TESTING": True})
        return app

    @pytest.fixture()
    def async_client(self, app) -> AsyncTestClient:
        return AsyncTestClient(app, Response, True)

    @pytest.fixture
    def file_operations_service(self) -> FileOperations:
        return FileOperations.get_class()

    @pytest.mark.asyncio
    async def test_request_root(
        self,
        async_client,
        mocker,
        test_file_movie_category,
        test_file_movie_category_bytes,
    ):
        mock_async_get = mocker.patch.object(AsyncBaseApi, "get")
        mock_async_get.return_value = test_file_movie_category
        mock_write_to_file = mocker.patch.object(FileOperations, "write_to_file")
        mock_read_file_to_bytes = mocker.patch.object(
            FileOperations, "read_file_to_bytes"
        )
        mock_read_file_to_bytes.return_value = test_file_movie_category_bytes
        mock_upload_to_cloud = mocker.patch.object(FileOperations, "upload_to_cloud")

        response = await async_client.get("/")
        mock_async_get.called_count == 10
        mock_write_to_file.called_count == 10
        mock_read_file_to_bytes.called_count == 10
        mock_upload_to_cloud.called_count == 10

        assert (
            response.text
            == "<h1>Executing Movie Category Extract To File & Cloud Storage For ['action-adventure', 'animation', 'classic', 'comedy', 'drama', 'horror', 'family', 'mystery', 'scifi-fantasy', 'western']</h2>"  # noqa: 501  pylint: disable=line-too-long
        )
        assert response.status_code == 200
