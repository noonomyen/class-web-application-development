from os import environ
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.resolve().parent.joinpath(".env"))

__all__ = [
    "IS_SERVERLESS",
    # "SUPPORT_DATABASE",
    "SECRET_KEY"
]

IS_SERVERLESS: bool = False if "IS_SERVERLESS" in environ and environ["IS_SERVERLESS"].strip().lower() == "false" else True
# SUPPORT_DATABASE: bool = True
assert "SECRET_KEY" in environ, "Missing SECRET_KEY in environment variables"
SECRET_KEY: str = environ["SECRET_KEY"]
