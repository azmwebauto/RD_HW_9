import logging

import httpx

from app import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Service:
    __client = httpx.AsyncClient(follow_redirects=True, timeout=20)

    @classmethod
    async def patch_cve(cls, cve_id: str, data: dict):
        url = f'{config.URL_TO_SERVICE}/cves/cve_id/{cve_id}'
        response = await cls.__client.patch(url, json=data)
        return response

    @classmethod
    async def post_data(cls, results: list[dict]) -> httpx.Response:
        try:
            logging.info(results)
            results = tuple(results)
            """
            POST http://localhost:8000/cves/
    
            {"data": {}}
            response from POST http://localhost:8000/cves/
            :return: httpx.Response
            """
            url = f'{config.URL_TO_SERVICE}/cves/'
            response = await cls.__client.post(url, json={'data': tuple(results)})
            logging.debug(response.status_code)
            return response
        except Exception as error:
            logging.exception(error)
        return None

    @classmethod
    async def get_data(cls) -> httpx.Response:
        """
        response from GET http://localhost:8000/cves/
        :return: httpx.Response
        """
        url = f'{config.URL_TO_SERVICE}/cves/'
        response = await cls.__client.get(url)
        logging.debug(response.status_code)
        return response

    @classmethod
    async def get_status(cls) -> httpx.Response:
        """
        response from GET http://localhost:8000/status/
        :return: httpx.Response
        """
        url = f'{config.URL_TO_SERVICE}/status'
        response = await cls.__client.get(url)
        logging.debug(response.status_code)
        return response


class GitHubInterface:
    __client = httpx.AsyncClient(follow_redirects=True, timeout=20)

    @classmethod
    async def get_data(cls, url) -> httpx.Response:
        response = await cls.__client.get(url)
        logging.debug(response.status_code)
        return response
