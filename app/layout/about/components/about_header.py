from dash import html


def build_header(title, subtitle):
    return html.Div(
        className="module-header", children=[html.H2(title), html.P(subtitle)]
    )
