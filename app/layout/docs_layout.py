from dash import html, dcc
from core.ui.styled_components import (
    styled_dropdown,
    styled_button
)

docs_section = html.Div(
    id="docs-container",
    children=[

        # ───────────────────────────────────────────────
        # Encabezado del módulo
        # ───────────────────────────────────────────────
        html.Div(
            className="module-header",
            children=[
                html.H2("Documentación Teórica"),
                html.P("Consulta la teoría de cada método disponible en NA‑Engine."),
            ],
        ),

        # ───────────────────────────────────────────────
        # Selección de módulo
        # ───────────────────────────────────────────────
        html.Div(className="module-card", children=[
            html.Label("Módulo"),
            styled_dropdown(
                id="docs-module",
                options=[
                    {"label": "Derivadas", "value": "numerical_derivative"},
                    {"label": "Interpolación", "value": "interpolation"},
                    {"label": "Integración", "value": "integration"},
                    {"label": "Álgebra Lineal", "value": "linear_algebra"},
                    {"label": "Ecuaciones No Lineales", "value": "nonlinear"},
                    {"label": "Ecuaciones Diferenciales (ODE)", "value": "ode"},
                ],
                placeholder="Selecciona un módulo",
            ),
        ]),

        # ───────────────────────────────────────────────
        # Selección de método
        # ───────────────────────────────────────────────
        html.Div(className="module-card", id="docs-method-card", children=[
            html.Label("Método"),
            styled_dropdown(
                id="docs-method",
                placeholder="Selecciona un método",
            ),
        ]),

        # ───────────────────────────────────────────────
        # Botón de cargar documentación
        # ───────────────────────────────────────────────
        html.Div(className="module-card", id="docs-btn-card", hidden=True, children=[
            styled_button(
                id="docs-run-btn",
                label="Mostrar documentación",
                kind="primary",
            ),
        ]),

        # ───────────────────────────────────────────────
        # Área donde se renderiza el markdown
        # ───────────────────────────────────────────────
        html.Div(id="docs-result-area", className="result-area"),
    ],
)
