import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.resolve().joinpath("..")))

from api import app
