import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.resolve()))

from api import app

if __name__ == "__main__":
    if "--debug" in sys.argv:
        app.run(debug=True)
    else:
        app.run()
