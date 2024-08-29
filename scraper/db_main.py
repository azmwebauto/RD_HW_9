import abc
import argparse
import asyncio
import logging
import os
import time
from typing import Generator

from sqlalchemy import insert

from scraper import serializers
from web_app import db as database
from web_app.cves import models

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class SaveToDatabaseInterface(abc.ABC):
    @abc.abstractmethod
    async def call(self, *args, **kwargs):
        pass


class SaveToDatabaseSQLAlchemy(SaveToDatabaseInterface):

    async def call(self, *args, **kwargs):
        return await self.save_to_db(*args, **kwargs)

    @staticmethod
    async def save_to_db(results: Generator[dict, None, None]):
        async with database.make_session(database.ENGINE) as session:
            try:
                await session.execute(insert(models.CveModel), results)
                await session.commit()
            except Exception as e:
                logging.error(e)
                await session.rollback()


class SaveToDatabaseWithAPI(SaveToDatabaseInterface):
    async def call(self, *args, **kwargs):
        return await self.save_to_db(*args, **kwargs)

    @staticmethod
    async def save_to_db(results: Generator[dict, None, None]):
        raise NotImplementedError('Not implemented yet')


async def main(filepath: str, max_open_file_limit: int = 1000):
    logging.info(filepath)

    files = tuple(os.path.join(root, file) for root, dirs, files in os.walk(filepath) for file in files if
                  file.endswith(".json") and 'delta' not in file)
    saving_tasks = [
        asyncio.create_task(
            saving_strategy.call(
                filter(
                    lambda file: file is not None,
                    (
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


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True)
    parser.add_argument('-max', '--max_open_file_limit',
                        type=int, default=1000, help='Maximum number of open files')
    return parser.parse_args()


if __name__ == '__main__':
    saving_strategy = SaveToDatabaseWithAPI

    start = time.perf_counter()
    args = get_args()
    asyncio.run(main(args.file, args.max_open_file_limit))
    end = time.perf_counter()
    logging.info(f'Finished in {end - start:.2f} seconds')
