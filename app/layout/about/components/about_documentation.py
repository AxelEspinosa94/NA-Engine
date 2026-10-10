from dash import html


def build_documentation(title, description):
    return html.Div(
        className="card",
        children=[html.H3(title), html.Div([html.P(line) for line in description])],
    )
