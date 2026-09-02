from dash import html


class Tooltip:
    def __init__(self, text):
        self.text = text

    def render(self):
        return html.Span(
            className="na-tooltip",
            children=[
                html.Span(className="na-tooltip-icon"),  # iconito ℹ️
                html.Span(self.text, className="na-tooltip-content"),
            ],
        )
