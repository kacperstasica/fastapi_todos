from pathlib import Path

from starlette.config import Config

BASE_DIR = Path(__file__).parent

config = Config(".env")

DATABASE_URL = config("DATABASE_URL")
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
