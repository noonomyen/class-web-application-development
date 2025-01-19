from flask import Flask, Blueprint, render_template_string
from api import config

__all__ = [
    "compatibility_middle",
    "compatibility_status_page"
]

status_pages: list[tuple[str, str, bool]] = []

def compatibility_middle(app: Flask, blueprint: Blueprint, serverless: bool):
    @blueprint.before_request
    def _compatibility_middleware():
        if config.IS_SERVERLESS and not serverless:
            return f"This route is not supported in serverless mode.<br>Name: {blueprint.import_name}<br>Path: {blueprint.url_prefix}", 404

    assert blueprint.url_prefix
    status_pages.append((blueprint.name, blueprint.url_prefix, serverless))
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
                {% for page_name, url_prefix, serverless in status_pages %}
                <tr>
                    <td>{{ page_name }}</td>
                    <td><a href="{{ url_prefix }}">{{ url_prefix }}</a></td>
                    <td>{% if config.IS_SERVERLESS and not serverless %}Unsupport{% else %}OK{% endif %}</td>
                </tr>
                {% endfor %}
            </table>
            <p>Serverless: {{ 'True' if config.IS_SERVERLESS else 'False' }}</p>
        </body>
    </html>
    """, status_pages=status_pages, config=config)
