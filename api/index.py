# for vercel serverless function

import pathlib
import sys

# api.__file__
sys.path.append(str(pathlib.Path(__file__).parent.resolve().joinpath("..")))

from api import app
from flask import Flask

assert isinstance(app, Flask), "app must be a Flask instance"
