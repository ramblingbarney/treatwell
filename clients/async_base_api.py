from socket import AF_INET
import asyncio
import logging
from typing import Dict, Optional
from dataclasses import dataclass, field

from aiohttp import ClientSession, ClientTimeout, TCPConnector

from main.exceptions import exception_handler_asyncio

logging.basicConfig(level=logging.DEBUG)


@dataclass
class AsyncBaseApi:
    headers: dict = field(default_factory=dict)
    aiohttp_client: Optional[ClientSession] = field(default=None)

    def __post_init__(self):
        if isinstance(self.headers, dict):
            self.headers = {**self._get_default_headers(), **self.headers}
        else:
            self.headers = self._get_default_headers()

    def add_custom_header(self, key: str = None, value: str = None):
        self.headers.update({key: value})

    def clear_custom_headers(self):
        self.headers = self._get_default_headers()

    def _get_default_headers(self) -> Dict[str, any]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    @classmethod
    def get_aiohttp_client(cls) -> ClientSession:
        if cls.aiohttp_client is None:
            timeout = ClientTimeout(total=30)
            connector = TCPConnector(family=AF_INET, limit_per_host=10)
            cls.aiohttp_client = ClientSession(timeout=timeout, connector=connector)
            loop = asyncio.get_running_loop()  # get running loop
            loop.set_exception_handler(
                exception_handler_asyncio
            )  # set the exception custom handler

        return cls.aiohttp_client

    @classmethod
    async def close_aiohttp_client(cls) -> None:
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    async def get(self, url: str = None, params: Dict = None) -> Dict[str, any]:

        tasks = [
            self._execute_request(
                method="GET", url=url, params=params, headers=self.headers
            )
        ]
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as error:
            for task in tasks:
                if not task.done():
                    try:
                        await task
                    except Exception:
                        logging.info(error)

        return results

    async def get_many(self, urls: list[str], params: Dict = None) -> Dict[str, any]:

        tasks = [
            self._execute_request(
                method="GET", url=url, params=params, headers=self.headers
            )
            for url in urls
        ]

        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as error:
            for task in tasks:
                if not task.done():
                    try:
                        await task
                    except Exception:
                        logging.info(error)

        return results

    @classmethod
    async def _execute_request(
        cls,
        method: str = None,
        url: str = None,
        headers: Dict = None,
        params: Dict = None,
        body: str = None,
    ) -> Dict[str, any]:
        client = cls.get_aiohttp_client()
        response = {"status_code": None, "body": None, "error": None}

        await asyncio.sleep(1)

        try:
            async with client.request(
                method=method, url=url, headers=headers, params=params, data=body
            ) as http_response:
                response["body"] = (
                    await http_response.text() if http_response.text else None
                )
                response["status_code"] = http_response.status
                http_response.raise_for_status()
        except Exception as error:
            response["error"] = error
        return response
