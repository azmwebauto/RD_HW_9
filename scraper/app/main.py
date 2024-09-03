import asyncio
import logging
import os
import time
from datetime import datetime
from pathlib import Path

from git import Repo

from scraper.app import serializers, config, api_interface

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def main(max_open_file_limit: int = 1000):
    logging.info("Starting fetch_cve_data")

    if not Path('cvelistV5').exists():
        logging.info(f"Cloning repository from {config.REPO_URL} to {config.LOCAL_PATH}")
        Repo.clone_from(config.REPO_URL, config.LOCAL_PATH, depth=1)

        files = tuple(
            os.path.join(root, file)

            for root, dirs, files in os.walk('cvelistV5')
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
            for batched_files in serializers.batcher(files, batch_size=max_open_file_limit)
        ]
        await asyncio.gather(*saving_tasks)
    else:
        logging.info(f"Pulling latest changes in {config.LOCAL_PATH}")
        repo = Repo(config.LOCAL_PATH)
        start_time = datetime.now()
        repo.remotes.origin.pull()
        logging.info(f"Pull completed in {datetime.now() - start_time}")


if __name__ == '__main__':
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    logging.info(f'Finished in {end - start:.2f} seconds')
