import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.resolve()))

from api import config

is_main = __name__ == "__main__"
config.IS_SERVERLESS = not is_main

from api import app

if is_main:
    if "--debug" in sys.argv:
        app.run(debug=True)
    else:
        app.run()
