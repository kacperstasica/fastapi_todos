from pathlib import Path

from starlette.config import Config
from starlette.datastructures import Secret

BASE_DIR = Path(__file__).parent.parent.parent

config = Config(".env")

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
