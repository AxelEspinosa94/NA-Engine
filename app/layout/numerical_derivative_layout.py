from dash import html, dcc

derivative_section = html.Div(
    id="derivative-container",
    children=[

        # ───────────────────────────────────────────────
        # Encabezado del módulo
        # ───────────────────────────────────────────────
        html.Div(
            className="module-header",
            children=[
                html.H2("Derivación Numérica"),
                html.P("Derivadas de primer, segundo y tercer orden, Richardson y parciales."),
            ],
        ),

        # ───────────────────────────────────────────────
        # Selector de método
        # ───────────────────────────────────────────────
        html.Div(className="card", children=[
            html.Label("Método"),
            dcc.Dropdown(
                id="deriv-method",
                options=[
                    {"label": "Forward",            "value": "forward"},
                    {"label": "Backward",           "value": "backward"},
                    {"label": "Central",            "value": "central"},
                    {"label": "Richardson",         "value": "richardson"},
                    {"label": "2da Forward",        "value": "second_forward"},
                    {"label": "2da Central",        "value": "second_central"},
                    {"label": "3ra Forward",        "value": "third_forward"},
                    {"label": "Parcial ∂/∂x",       "value": "partial_x"},
                    {"label": "Parcial ∂/∂y",       "value": "partial_y"},
                ],
                placeholder="Selecciona un método",
                className="input",
            ),
        ]),

        # ───────────────────────────────────────────────
        # Modo de entrada (siempre función)
        # ───────────────────────────────────────────────
        html.Div(className="card", id="deriv-mode-card", children=[
            html.Label("Modo de entrada"),
            dcc.RadioItems(
                id="deriv-input-mode",
                options=[{"label": "Función f(x)", "value": "function"}],
                value="function",
                className="radio-group",
                inline=True,
            ),
        ]),

        # ───────────────────────────────────────────────
        # Área dinámica de input
        # ───────────────────────────────────────────────
        html.Div(id="deriv-input-area", className="card input-area"),

        # ───────────────────────────────────────────────
        # Input para y (solo visible en parciales)
        # ───────────────────────────────────────────────
        html.Div(className="card", id="deriv-y-card", hidden=True, children=[
            html.Label("Valor de y"),
            dcc.Input(
                id="deriv-y",
                type="number",
                placeholder="ej: 3.0",
                className="input",
            ),
        ]),

        # ───────────────────────────────────────────────
        # Botón de ejecución
        # ───────────────────────────────────────────────
        html.Div(className="card", id="deriv-btn-card", hidden=True, children=[
            html.Button("Calcular", id="deriv-run-btn", className="btn-primary"),
        ]),

        # ───────────────────────────────────────────────
        # Área de resultados
        # ───────────────────────────────────────────────
        html.Div(id="deriv-result-area", className="result-area"),
    ],
)
