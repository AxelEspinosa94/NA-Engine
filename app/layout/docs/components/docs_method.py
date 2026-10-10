from dash import html

from core.ui.styled_components import styled_dropdown


def docs_method_selector(options=None):
    return html.Div(
        className="module-card",
        id="docs-method-card",
        children=[
            html.Label("Método"),
            styled_dropdown(
                id="docs-method",
                options=options,
                placeholder="Selecciona un método",
            ),
        ],
    )
