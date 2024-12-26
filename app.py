from sys import argv

from api.index import app

if __name__ == "__main__":
    if "--debug" in argv:
        app.run(debug=True)
    else:
        app.run()
