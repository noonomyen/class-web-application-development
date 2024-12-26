import sys
sys.path.append("./api")

from flask import Flask, redirect

from calculator import calculator_blueprint

app = Flask(__name__)

app = Flask(
    __name__,
    static_url_path="",
    static_folder="../static",
    template_folder="../templates"
)

app.register_blueprint(calculator_blueprint, url_prefix="/assignments/2/calculator")

@app.route("/")
def index():
    return redirect("https://github.com/noonomyen/class-web-application-development", 302)
