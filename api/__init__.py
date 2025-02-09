from flask import Flask, redirect
from pathlib import Path
from api import config

__all__ = ["app"]

app = Flask(__name__)

app = Flask(
    __name__,
    static_url_path="",
    static_folder="../static",
    template_folder="../templates"
)

app.secret_key = config.SECRET_KEY

curr_dir = Path(__file__).parent.resolve()

for file in (curr_dir / "blueprints").iterdir():
    if file.name == "__pycache__": continue

    module = __import__(f"api.blueprints.{file.stem}", fromlist=["serverless", "blueprint"])
    assert all((n in module.__dict__) for n in ("serverless", "blueprint")), f"Missing required variables in {file.name}"
    assert module.blueprint.url_prefix, "Require blueprint.url_prefix"
    app.register_blueprint(module.blueprint)

@app.route("/")
def index():
    return redirect("index.html")

from api.db import football_clubs_db

app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI

football_clubs_db.init_app(app)
