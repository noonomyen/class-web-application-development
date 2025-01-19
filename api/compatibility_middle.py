from flask import Flask, Blueprint, render_template_string
from api import config

__all__ = [
    "compatibility_middle",
    "compatibility_status_page"
]

status_pages: list[tuple[str, str, str]] = [("Dummy Blueprint", "/assignments/test", "Unsupport")]

# dummy blueprint

dummy_blueprint = Blueprint("dummy_blueprint", __name__)
@dummy_blueprint.before_request
def _compatibility_middleware_dummy_blueprint():
    return f"This route is not supported for {dummy_blueprint.import_name + '.' + dummy_blueprint.name}", 404

@dummy_blueprint.route("/")
def _dummy_blueprint_root():
    return "Test"

#

def compatibility_middle(app: Flask, blueprint: Blueprint, serverless: bool):
    @blueprint.before_request
    def _compatibility_middleware():
        if config.IS_SERVERLESS and not serverless:
            return f"This route is not supported in serverless mode.<br>Path: {blueprint.import_name}.{blueprint.url_prefix}", 404

    assert blueprint.url_prefix
    status_pages.append((blueprint.name, blueprint.url_prefix, "Unsupport" if config.IS_SERVERLESS and not serverless else "OK"))
    app.register_blueprint(blueprint)

compatibility_status_page = Blueprint("Compatibility Status", __name__)

@compatibility_status_page.route("/")
def assignments():
    return render_template_string("""
    <html>
        <head>
            <title>Compatibility Status</title>
            <style>
                table, th, td {
                    border: 1px solid black;
                    border-collapse: collapse;
                    padding: 5px;
                }
            </style>
        </head>
        <body>
            <h1>Compatibility Status</h1>
            <table>
                <tr>
                    <th>Page Name</th>
                    <th>URL Prefix</th>
                    <th>Status</th>
                </tr>
                {% for page_name, url_prefix, status in status_pages %}
                <tr>
                    <td>{{ page_name }}</td>
                    <td><a href="{{ url_prefix }}">{{ url_prefix }}</a></td>
                    <td>{{ status }}</td>
                </tr>
                {% endfor %}
            </table>
            <p>Serverless: {{ 'True' if config.IS_SERVERLESS else 'False' }}</p>
        </body>
    </html>
    """, status_pages=status_pages, config=config)
