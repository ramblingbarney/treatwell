import pytest
import pytest_asyncio

from clients.async_base_api import AsyncBaseApi

from aiohttp import ClientSession
from unittest import mock


class TestAsyncBaseClient:
    @pytest_asyncio.fixture(scope="class")
    async def client(self):
        client = AsyncBaseApi()
        yield client
        await client.close_aiohttp_client()

    @pytest.mark.asyncio
    async def test_get_default_headers(self, client):
        headers = client._get_default_headers()
        assert len(headers) == 2
        assert "Accept" in headers.keys()
        assert client.headers["Accept"] == "application/json"
        assert "Content-Type" in headers.keys()
        assert client.headers["Content-Type"] == "application/json"

    @pytest.mark.asyncio
    async def test_add_custom_header(self, client):
        client.add_custom_header("x-customheader", "custom value")
        assert "x-customheader" in client.headers.keys()
        assert client.headers["x-customheader"] == "custom value"

    @pytest.mark.asyncio
    async def test_clear_custom_headers(self, client):
        client.add_custom_header("x-customheader", "custom value")
        assert "x-customheader" in client.headers.keys()

        client.clear_custom_headers()
        assert ("x-customheader" in client.headers.keys()) is False
        assert "Accept" in client.headers.keys()
        assert "Content-Type" in client.headers.keys()

    @pytest.mark.asyncio
    @mock.patch.object(ClientSession, "request")
    async def test_get_returns_error(self, mock_client_session, client):
        mock_client_session.side_effect = Exception("Some Error")
        response = await client.get(url="http://testserver")
        mock_client_session.assert_called_once()
        assert str(response[0]["error"]) == "Some Error"

    @pytest.mark.asyncio
    @mock.patch.object(ClientSession, "request")
    async def test_get_many_returns_error(self, mock_client_session, client):
        mock_client_session.side_effect = Exception("Some Error")
        response = await client.get_many(
            urls=["http://testserver", "http://testserver1"]
        )
        mock_client_session.called_count == 2
        assert str(response[0]["error"]) == "Some Error"

    @pytest.mark.asyncio
    @mock.patch.object(ClientSession, "request")
    async def test_get_returns_expected_response(self, mock_client_session, client):
        mock_client_session.return_value.__aenter__.return_value.status = 200
        mock_client_session.return_value.__aenter__.return_value.text.return_value = (
            '{"Test": "Get"}'
        )
        response = await client.get(url="http://testserver")
        mock_client_session.assert_called_once()
        assert str(response[0]["body"]) == '{"Test": "Get"}'

    @pytest.mark.asyncio
    @mock.patch.object(ClientSession, "request")
    async def test_get_many_returns_expected_response(
        self, mock_client_session, client
    ):
        mock_client_session.return_value.__aenter__.return_value.status = 200
        mock_client_session.return_value.__aenter__.return_value.text.return_value = (
            '{"Test": "Get"}'
        )
        response = await client.get_many(
            urls=["http://testserver", "http://testserver1"]
        )
        mock_client_session.called_count == 2
        assert str(response[0]["body"]) == '{"Test": "Get"}'
