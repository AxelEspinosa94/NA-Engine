# layout/docs_section.py

from dash import html, dcc

docs_section = html.Div(
    id="docs-container",
    children=[

        html.Div(
            className="module-header",
            children=[
                html.H2("Documentación Teórica"),
                html.P("Consulta la teoría de cada método disponible en NA‑Engine."),
            ],
        ),

        # Selección de módulo
        html.Div(className="card", children=[
            html.Label("Módulo"),
            dcc.Dropdown(
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
                className="input",
            ),
        ]),

        # Selección de método
        html.Div(className="card", id="docs-method-card", children=[
            html.Label("Método"),
            dcc.Dropdown(
                id="docs-method",
                placeholder="Selecciona un método",
                className="input",
            ),
        ]),

        # Botón de cargar documentación
        html.Div(className="card", id="docs-btn-card", hidden=True, children=[
            html.Button("Mostrar documentación", id="docs-run-btn", className="btn-primary"),
        ]),

        # Área donde se renderiza el markdown
        html.Div(id="docs-result-area", className="result-area"),
    ],
)
