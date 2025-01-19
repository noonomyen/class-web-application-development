from os import environ
from flask import Flask, redirect
from pathlib import Path
from api.compatibility_middle import compatibility_middle, compatibility_status_page, dummy_blueprint

__all__ = ["app"]

app = Flask(__name__)

app = Flask(
    __name__,
    static_url_path="",
    static_folder="../static",
    template_folder="../templates"
)

app.secret_key = environ["SECRET_KEY"] if "SECRET_KEY" in environ else open("SECRET_KEY.txt", "r").read()

curr_dir = Path(__file__).parent.resolve()

for file in (curr_dir / "blueprints").glob("*.py"):
    if file.name != "__init__.py":
        module = __import__(f"api.blueprints.{file.stem}", fromlist=["serverless", "blueprint"])
        assert all((n in module.__dict__) for n in ("serverless", "blueprint")), f"Missing required variables in {file.name}"
        assert module.blueprint.url_prefix, "Require blueprint.url_prefix"
        compatibility_middle(app, module.blueprint, module.serverless)

app.register_blueprint(compatibility_status_page, url_prefix="/assignments")
app.register_blueprint(dummy_blueprint, url_prefix="/assignments/test")

@app.route("/")
def index():
    return redirect("index.html")
