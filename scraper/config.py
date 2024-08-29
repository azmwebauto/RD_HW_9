import logging
from pathlib import Path

from dotenv import load_dotenv

# Root folder path
ROOT_DIR = Path(__file__).parent.parent.absolute()

# Env path
load_dotenv(ROOT_DIR / '.env')

# Redis config
REDIS_URI = f''

# logging config
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
