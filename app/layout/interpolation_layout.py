from dash import html, dcc

interpolation_section = html.Div(
    id="interpolation-container",
    children=[

        html.Div(
            className="module-header",
            children=[
                html.H2("Interpolación Numérica"),
                html.P("Lagrange, Newton, Hermite y Splines Cúbicos."),
            ],
        ),

        # ── Selector de método ──────────────────────────────────────
        html.Div(className="card", children=[
            html.Label("Método"),
            dcc.Dropdown(
                id="interp-method",
                options=[
                    {"label": "Lagrange",        "value": "lagrange"},
                    {"label": "Newton",           "value": "newton"},
                    {"label": "Hermite",          "value": "hermite"},
                    {"label": "Splines Cúbicos",  "value": "spline_cubic"},
                ],
                placeholder="Selecciona un método",
                className="input",
            ),
        ]),

        # ── Selector de modo de input ────────────────────────────────
        html.Div(className="card", id="interp-mode-card", hidden=True, children=[
            html.Label("Modo de entrada"),
            dcc.RadioItems(
                id="interp-input-mode",
                options=[
                    {"label": "Función f(x)", "value": "function"},
                    {"label": "Tabla manual", "value": "table"},
                    {"label": "Subir archivo", "value": "upload"},
                ],
                value="table",
                className="radio-group",
                inline=True,
            ),
        ]),

        # ── Área dinámica de input ───────────────────────────────────
        html.Div(id="interp-input-area", className="card input-area"),

        # ── xk ──────────────────────────────────────────────────────
        html.Div(className="card", id="interp-xk-card", hidden=True, children=[
            html.Label("Valor a evaluar (xk)"),
            dcc.Input(
                id="interp-xk",
                type="number",
                placeholder="ej: 1.5",
                className="input",
            ),
        ]),

        # ── Botón ────────────────────────────────────────────────────
        html.Div(className="card", id="interp-btn-card", hidden=True, children=[
            html.Button("Calcular", id="interp-run-btn", className="btn-primary"),
        ]),

        # ── Resultado ────────────────────────────────────────────────
        html.Div(id="interp-result-area", className="result-area"),
    ],
)