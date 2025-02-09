from os import environ
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).parent.resolve().parent.joinpath(".env"))
except ImportError:
    pass

__all__ = [
    "SECRET_KEY",
    "SQLALCHEMY_DATABASE_URI"
]

assert "SECRET_KEY" in environ, "Missing SECRET_KEY in environment variables"
SECRET_KEY: str = environ["SECRET_KEY"]
SQLALCHEMY_DATABASE_URI: str = environ["SQLALCHEMY_DATABASE_URI"]
