import pathlib
import sys

app_dir = pathlib.Path(__file__).parent.resolve()
sys.path.append(str(app_dir))

from api import app

if __name__ == "__main__":
    if "--debug" in sys.argv:
        app.run(debug=True)
    else:
        app.run()
