from dash import html, dcc

nonlinear_section = html.Div(
    id="nonlinear-container",
    children=[

        # ───────────────────────────────────────────────
        # Encabezado del módulo
        # ───────────────────────────────────────────────
        html.Div(
            className="module-header",
            children=[
                html.H2("Ecuaciones No Lineales"),
                html.P("Métodos de Bisección, Falsa Posición, Secante, Newton y Punto Fijo."),
            ],
        ),

        # ───────────────────────────────────────────────
        # Selector de método
        # ───────────────────────────────────────────────
        html.Div(className="card", children=[
            html.Label("Método"),
            dcc.Dropdown(
                id="nonlin-method",
                options=[
                    {"label": "Bisección",        "value": "bisection"},
                    {"label": "Falsa Posición",  "value": "false_position"},
                    {"label": "Newton",          "value": "newton"},
                    {"label": "Secante",         "value": "secant"},
                    {"label": "Punto Fijo",      "value": "fixed_point"},
                ],
                placeholder="Selecciona un método",
                className="input",
            ),
        ]),

        # ───────────────────────────────────────────────
        # Modo de entrada (siempre función)
        # ───────────────────────────────────────────────
        html.Div(className="card", id="nonlin-mode-card", children=[
            html.Label("Modo de entrada"),
            dcc.RadioItems(
                id="nonlin-input-mode",
                options=[{"label": "Función f(x)", "value": "function"}],
                value="function",
                className="radio-group",
                inline=True,
            ),
        ]),

        # ───────────────────────────────────────────────
        # Área dinámica de input
        # ───────────────────────────────────────────────
        html.Div(id="nonlin-input-area", className="card input-area"),

        # ───────────────────────────────────────────────
        # Input g(x) — solo para punto fijo
        # ───────────────────────────────────────────────
        html.Div(className="card", id="nonlin-g-card", hidden=True, children=[
            html.Label("Función g(x)"),
            dcc.Input(
                id="nonlin-g",
                type="text",
                placeholder="ej: 0.5*(x + 5/x)",
                className="input",
            ),
        ]),

        # ───────────────────────────────────────────────
        # Input x1 — solo para secante
        # ───────────────────────────────────────────────
        html.Div(className="card", id="nonlin-x1-card", hidden=True, children=[
            html.Label("Valor inicial x1"),
            dcc.Input(
                id="nonlin-x1",
                type="number",
                placeholder="ej: 3.0",
                className="input",
            ),
        ]),

        # ───────────────────────────────────────────────
        # Intervalo [a, b] — bisección y falsa posición
        # ───────────────────────────────────────────────
        html.Div(className="card", id="nonlin-interval-card", hidden=True, children=[
            html.Label("Intervalo [a, b]"),
            html.Div(className="input-row", children=[
                dcc.Input(id="nonlin-a", type="number", placeholder="a", className="input"),
                dcc.Input(id="nonlin-b", type="number", placeholder="b", className="input"),
            ]),
        ]),

        # ───────────────────────────────────────────────
        # Botón de ejecución
        # ───────────────────────────────────────────────
        html.Div(className="card", id="nonlin-btn-card", hidden=True, children=[
            html.Button("Calcular", id="nonlin-run-btn", className="btn-primary"),
        ]),

        # ───────────────────────────────────────────────
        # Área de resultados
        # ───────────────────────────────────────────────
        html.Div(id="nonlin-result-area", className="result-area"),
    ],
)
