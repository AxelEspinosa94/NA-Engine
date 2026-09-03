from dash import html

from core.ui.styled_components import styled_dropdown


def docs_module_selector(options):
    return html.Div(
        className="module-card",
        children=[
            html.Label("Módulo"),
            styled_dropdown(
                id="docs-module",
                options=options,
                placeholder="Selecciona un módulo",
            ),
        ],
    )
