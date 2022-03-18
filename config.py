from pathlib import Path

from starlette.config import Config

BASE_DIR = Path(__file__).parent

config = Config(".env")

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
