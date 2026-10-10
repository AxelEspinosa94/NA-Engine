from dash import html


def build_changelog(title, items):
    return html.Div(
        className="card",
        children=[
            html.H3(title),
            html.Div(
                className="about-info-box",
                children=[html.Ul([html.Li(item) for item in items])],
            ),
        ],
    )
