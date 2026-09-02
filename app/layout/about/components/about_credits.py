from dash import html


def build_credits(title, description):
    return html.Div(
        className="card",
        children=[
            html.H3(title),
            html.Div(
                className="about-info-box",
                children=[html.P(line) for line in description],
            ),
        ],
    )
