from flask import Flask, redirect

app = Flask(__name__)

app = Flask(
    __name__,
    static_url_path="",
    static_folder="../static",
    template_folder="../templates"
)

@app.route("/")
def index():
    return redirect("https://github.com/noonomyen/class-web-application-development", 302)
