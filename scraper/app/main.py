import asyncio
import logging
import time

from app import clone_repo, pull_repo

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def main():
    await clone_repo.main()
    await pull_repo.main()


if __name__ == '__main__':
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    logging.info(f'Finished in {end - start:.2f} seconds')
