import asyncio
import logging
import os
import time
from pathlib import Path

from git import Repo

from app import serializers, config, api_interface

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


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


async def main():
    if not Path(config.LOCAL_PATH).exists():
        logging.info('Pulling all CVEs')
        logging.info(f"Cloning repository from {config.REPO_URL} to {config.LOCAL_PATH}")
        Repo.clone_from(config.REPO_URL, config.LOCAL_PATH, depth=1)
        await post_new_cves()
    else:
        logging.info('Cves found in local repository')


if __name__ == '__main__':
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    logging.info(f'Finished in {end - start:.2f} seconds')
