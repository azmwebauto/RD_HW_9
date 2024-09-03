import logging
import os
from pathlib import Path

from dotenv import load_dotenv

# Root folder path
ROOT_DIR = Path(__file__).parent.parent.absolute()

# Env path
load_dotenv(ROOT_DIR / '.env')

# Redis config
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_USER = os.getenv('REDIS_USER')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_URI = f'redis://{REDIS_USER}:{REDIS_PORT}@{REDIS_HOST}:{REDIS_PORT}'

# logging config
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# App Config
URL_TO_SERVICE = os.getenv('URL_TO_SERVICE')


REPO_URL = 'https://github.com/CVEProject/cvelistV5'
LOCAL_PATH = ROOT_DIR / 'cvelistV5'


SCRAPING_SCHEDULE_IN_MINUTES = os.getenv('SCRAPING_SCHEDULE_IN_MINUTES')

MAX_POSTING_LIMIT = int(os.getenv('MAX_POSTING_LIMIT'))
