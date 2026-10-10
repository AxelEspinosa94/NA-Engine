from dash import html

from core.ui.styled_components import styled_button


def docs_button():
    return html.Div(
        className="module-card",
        id="docs-btn-card",
        hidden=True,
        children=[
            styled_button(
                id="docs-run-btn",
                label="Mostrar documentación",
                kind="primary",
            ),
        ],
    )
