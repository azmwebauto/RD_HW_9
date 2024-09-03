import logging
from typing import Generator

import httpx

from scraper.app import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Service:
    __client = httpx.AsyncClient()

    @classmethod
    async def post_data(cls, results: Generator[dict, None, None]) -> httpx.Response:
        """
        POST http://localhost:8000/cves

        {"data": {}}
        response from POST http://localhost:8000/cves
        :return: httpx.Response
        """
        url = f'{config.URL_TO_SERVICE}/cves'
        response = await cls.__client.post(url, json={'data': list(results)})
        logging.debug(response.status_code)
        return response

    @classmethod
    async def get_data(cls) -> httpx.Response:
        """
        response from GET http://localhost:8000/cves
        :return: httpx.Response
        """
        url = f'{config.URL_TO_SERVICE}/cves'
        response = await cls.__client.get(url)
        logging.debug(response.status_code)
        return response

    @classmethod
    async def get_status(cls) -> httpx.Response:
        """
        response from GET http://localhost:8000/status
        :return: httpx.Response
        """
        url = f'{config.URL_TO_SERVICE}/status'
        response = await cls.__client.get(url)
        logging.debug(response.status_code)
        return response
