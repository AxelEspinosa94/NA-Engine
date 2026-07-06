from dash import html, dcc

integration_section = html.Div(
    id="integration-container",
    children=[

        # ───────────────────────────────────────────────
        # Encabezado del módulo
        # ───────────────────────────────────────────────
        html.Div(
            className="module-header",
            children=[
                html.H2("Integración Numérica"),
                html.P("Trapecio, Simpson, Romberg y Gauss-Legendre."),
            ],
        ),

        # ───────────────────────────────────────────────
        # Selector de método
        # ───────────────────────────────────────────────
        html.Div(className="card", children=[
            html.Label("Método"),
            dcc.Dropdown(
                id="integr-method",
                options=[
                    {"label": "Trapecio Simple",      "value": "trapezoid_simple"},
                    {"label": "Trapecio Compuesto",   "value": "trapezoid_composite"},
                    {"label": "Simpson 1/3",          "value": "simpson_1_3"},
                    {"label": "Simpson 3/8",          "value": "simpson_3_8"},
                    {"label": "Romberg",              "value": "romberg"},
                    {"label": "Gauss-Legendre",       "value": "gauss"},
                ],
                placeholder="Selecciona un método",
                className="input",
            ),
        ]),

        # ───────────────────────────────────────────────
        # Modo de entrada (siempre función)
        # ───────────────────────────────────────────────
        html.Div(className="card", id="integr-mode-card", children=[
            html.Label("Modo de entrada"),
            dcc.RadioItems(
                id="integr-input-mode",
                options=[{"label": "Función f(x)", "value": "function"}],
                value="function",
                className="radio-group",
                inline=True,
            ),
        ]),

        # ───────────────────────────────────────────────
        # Área dinámica de input
        # ───────────────────────────────────────────────
        html.Div(id="integr-input-area", className="card input-area"),

        # ───────────────────────────────────────────────
        # Gauss-Legendre: número de puntos
        # ───────────────────────────────────────────────
        html.Div(className="card", id="integr-gauss-card", hidden=True, children=[
            html.Label("Puntos de Gauss-Legendre"),
            dcc.Input(
                id="integr-gauss-points",
                type="number",
                placeholder="ej: 2",
                className="input",
            ),
        ]),

        # ───────────────────────────────────────────────
        # Botón de ejecución
        # ───────────────────────────────────────────────
        html.Div(className="card", id="integr-btn-card", hidden=True, children=[
            html.Button("Calcular", id="integr-run-btn", className="btn-primary"),
        ]),

        # ───────────────────────────────────────────────
        # Área de resultados
        # ───────────────────────────────────────────────
        html.Div(id="integr-result-area", className="result-area"),
    ],
)
