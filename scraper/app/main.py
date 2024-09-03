import asyncio
import json
import logging
import os
import time
from pathlib import Path

import aiofiles
from git import Repo

from app import serializers, config, api_interface

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def main():
    logging.info("Starting fetch_cve_data")
    get_status_response = await api_interface.Service.get_status()
    assert get_status_response.is_success
    assert get_status_response.text == 'OK'

    if not Path(config.LOCAL_PATH).exists():
        logging.info('Pulling all CVEs')
        logging.info(f"Cloning repository from {config.REPO_URL} to {config.LOCAL_PATH}")
        Repo.clone_from(config.REPO_URL, config.LOCAL_PATH, depth=1)
        await post_new_cves()
    else:
        logging.info(f"Pulling latest changes in {config.LOCAL_PATH}")
        Repo(config.LOCAL_PATH).remotes.origin.pull()
        await update_existing_using_delta()


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


async def post_new_cves():

    logging.info('Posting all cves to service')
    files = tuple(
        os.path.join(root, file)

        for root, dirs, files in os.walk(config.LOCAL_PATH)
        for file in files
        if file.endswith(".json") and 'delta' not in file
    )
    saving_tasks = [
        asyncio.create_task(
            api_interface.Service.post_data(
                filter(
                    lambda file: file is not None, (
                        serializers.serialize_cve_record(file)
                        for file in await asyncio.gather(
                        *tuple(serializers.parse_json(file) for file in batched_files)
                    )
                    )
                )
            )
        )
        for batched_files in serializers.batcher(files, batch_size=config.MAX_POSTING_LIMIT)
    ]
    await asyncio.gather(*saving_tasks)


if __name__ == '__main__':
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    logging.info(f'Finished in {end - start:.2f} seconds')
