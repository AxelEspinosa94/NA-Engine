from dash import html, dcc

ode_section = html.Div(
    id="ode-container",
    children=[

        # ───────────────────────────────────────────────
        # Encabezado del módulo
        # ───────────────────────────────────────────────
        html.Div(
            className="module-header",
            children=[
                html.H2("Ecuaciones Diferenciales Ordinarias (ODE)"),
                html.P("Métodos IVP, sistemas, shooting y diferencias finitas."),
            ],
        ),

        # ───────────────────────────────────────────────
        # Selector de método
        # ───────────────────────────────────────────────
        html.Div(className="card", children=[
            html.Label("Método"),
            dcc.Dropdown(
                id="ode-method",
                options=[
                    {"label": "Euler",                 "value": "euler"},
                    {"label": "Heun",                  "value": "heun"},
                    {"label": "Runge–Kutta 2",         "value": "rk2"},
                    {"label": "Runge–Kutta 4",         "value": "rk4"},
                    {"label": "RK4 Sistema",           "value": "rk4_system"},
                    {"label": "Shooting (BVP)",        "value": "shooting"},
                    {"label": "Diferencias Finitas",   "value": "finite_differences"},
                    {"label": "Adams–Bashforth 2",     "value": "adams_bashforth_2"},
                    {"label": "Adams–Bashforth 3",     "value": "adams_bashforth_3"},
                    {"label": "Adams–Moulton 2",       "value": "adams_moulton_2"},
                ],
                placeholder="Selecciona un método",
                className="input",
            ),
        ]),

        # ───────────────────────────────────────────────
        # Selector de modo de entrada
        # ───────────────────────────────────────────────
        html.Div(className="card", children=[
            html.Label("Modo de entrada"),
            dcc.RadioItems(
                id="ode-input-mode",
                options=[
                    {"label": "Función f(x, y)", "value": "function"},
                    {"label": "Sistema",         "value": "system"},
                ],
                value="function",
                className="radio-group",
                inline=True,
            ),
        ]),

        # ───────────────────────────────────────────────
        # Área dinámica de input (función o sistema)
        # ───────────────────────────────────────────────
        html.Div(id="ode-input-area", className="card input-area", children = [
            # ───────────────────────────────────────────────
            # Campo de input para función f(x, y)
            # ───────────────────────────────────────────────
            html.Div(id= "ode-function-card",
                children=[
                    html.Label("f(x, y)"),
                    dcc.Input(
                        id="ode-function",
                        type="text",
                        placeholder="Ej: x + y",
                        className="input",
                    ),
                ]
            ),
            # ───────────────────────────────────────────────
            # Campo de input para sistemass de ecuaciones
            # ───────────────────────────────────────────────
            html.Div(id = "ode-system-card", hidden=True,  # Initially hidden; shown when input_mode is "system"
                children=[
                    html.Label("Sistema de ecuaciones"),
                    dcc.Textarea(
                        id="ode-system",
                        placeholder="Ej:\ny1' = y2\ny2' = -y1",
                        className="textarea",
                    ),
                ]
            )
        ]),

        # ───────────────────────────────────────────────
        # Campos IVP (x0, y0, x_end, h)
        # ───────────────────────────────────────────────
        html.Div(id="ode-ivp-card", className="card", hidden=True, children=[
            html.Label("Condiciones iniciales"),
            html.Div(className="input-row", children=[
                html.Div(children=[
                    html.Label("x₀"),
                    dcc.Input(id="ode-x0", type="number", className="input"),
                ]),
                html.Div(children=[
                    html.Label("y₀"),
                    dcc.Input(id="ode-y0", type="number", className="input"),
                ]),
                html.Div(children=[
                    html.Label("x final"),
                    dcc.Input(id="ode-x-end", type="number", className="input"),
                ]),
                html.Div(children=[
                    html.Label("Paso h"),
                    dcc.Input(id="ode-h", type="number", className="input"),
                ]),
            ]),
        ]),

        # ───────────────────────────────────────────────
        # Campos para sistemas (y0 vector)
        # ───────────────────────────────────────────────
        html.Div(id="ode-system-y0-card", className="card", hidden=True, children=[
            html.Label("Vector inicial y₀"),
            dcc.Textarea(
                id="ode-y0-system",
                placeholder="Ej: 1, 0, -2",
                className="textarea",
            ),
        ]),

        # ───────────────────────────────────────────────
        # Campos BVP — Shooting
        # ───────────────────────────────────────────────
        html.Div(id="ode-shooting-card", className="card", hidden=True, children=[
            html.Label("Condiciones de frontera (Shooting)"),
            html.Div(className="input-row", children=[
                html.Div(children=[
                    html.Label("α = y(x₀)"),
                    dcc.Input(id="ode-alpha", type="number", className="input"),
                ]),
                html.Div(children=[
                    html.Label("β = y(x_end)"),
                    dcc.Input(id="ode-beta", type="number", className="input"),
                ]),
                html.Div(children=[
                    html.Label("Pendiente inicial s₀"),
                    dcc.Input(id="ode-s0", type="number", className="input"),
                ]),
            ]),
        ]),

        # ───────────────────────────────────────────────
        # Campos BVP — Diferencias finitas
        # ───────────────────────────────────────────────
        html.Div(id="ode-fd-card", className="card", hidden=True, children=[
            html.Label("Diferencias finitas"),
            html.Div(className="input-row", children=[
                html.Div(children=[
                    html.Label("α = y(x₀)"),
                    dcc.Input(id="ode-alpha-fd", type="number", className="input"),
                ]),
                html.Div(children=[
                    html.Label("β = y(x_end)"),
                    dcc.Input(id="ode-beta-fd", type="number", className="input"),
                ]),
                html.Div(children=[
                    html.Label("n (subdivisiones)"),
                    dcc.Input(id="ode-n", type="number", className="input"),
                ]),
            ]),
        ]),

        # ───────────────────────────────────────────────
        # Botón de ejecución
        # ───────────────────────────────────────────────
        html.Div(className="card", id="ode-btn-card", hidden=True, children=[
            html.Button("Calcular", id="ode-run-btn", className="btn-primary"),
        ]),

        # ───────────────────────────────────────────────
        # Área de resultados
        # ───────────────────────────────────────────────
        html.Div(id="ode-result-area", className="result-area"),
    ],
)
