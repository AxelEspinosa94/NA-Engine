from dash import html

from app.version import get_git_version


def build_version_card(title, description, version=None):
    version = version or get_git_version()

    return html.Div(
        className="card",
        children=[
            html.H3(title),
            html.Div([html.P(line) for line in description]),
            html.Div(
                id="about-version-display",
                className="about-info-box",
                children=[html.P(f"Installed version: {version}")],
            ),
        ],
    )
