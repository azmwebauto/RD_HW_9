import asyncio
import json
import logging
import time
from pathlib import Path

import aiofiles
from git import Repo

from app import serializers, config, api_interface

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def update_existing_using_delta():
    delta = config.LOCAL_PATH / 'cves' / 'delta.json'
    async with aiofiles.open(delta, mode='r') as delta_file:
        delta = await delta_file.read()
    delta_json = json.loads(delta)
    new = delta_json.get('new')
    updated = delta_json.get('updated')
    if new:
        github_links = [cve['githubLink'] for cve in new]
        responses = [asyncio.create_task(api_interface.GitHubInterface.get_data(link)) for link in github_links]
        responses = await asyncio.gather(*responses)
        data = [
            serializers.serialize_cve_record(response.json()) for response in responses if response.is_success
        ]
        post_response = await api_interface.Service.post_data(data)
        logging.info(f"Posting new cves to service {post_response.text}")
    if updated:
        github_links = [cve['githubLink'] for cve in updated]
        responses = [asyncio.create_task(api_interface.GitHubInterface.get_data(link)) for link in github_links]
        responses = await asyncio.gather(*responses)
        data = [
            serializers.serialize_cve_record(response.json()) for response in responses if response.is_success
        ]

        tasks = [api_interface.Service.patch_cve(row['cve_id'], row) for row in data]
        await asyncio.gather(*tasks)


async def main():
    if Path(config.LOCAL_PATH).exists():
        logging.info("Starting fetch_cve_data")
        get_status_response = await api_interface.Service.get_status()
        assert get_status_response.is_success
        assert get_status_response.text == 'OK'

        logging.info(f"Pulling latest changes in {config.LOCAL_PATH}")
        Repo(config.LOCAL_PATH).remotes.origin.pull()
        await update_existing_using_delta()
    else:
        logging.error("CVE folder not found")

if __name__ == '__main__':
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    logging.info(f'Finished in {end - start:.2f} seconds')
