from dash import html, dcc, dash_table

linear_algebra_section = html.Div(
    id="linear-algebra-container",
    children=[

        # ───────────────────────────────────────────────
        # Encabezado del módulo
        # ───────────────────────────────────────────────
        html.Div(
            className="module-header",
            children=[
                html.H2("Álgebra Lineal"),
                html.P("Operaciones matriciales y solución de sistemas de ecuaciones."),
            ],
        ),

        # ───────────────────────────────────────────────
        # Selector de tipo de operación
        # ───────────────────────────────────────────────
        html.Div(className="card", children=[
            html.Label("Tipo de operación"),
            dcc.RadioItems(
                id="la-calculation-type",
                options=[
                    {"label": "Operaciones con matrices", "value": "matrix_operations"},
                    {"label": "Sistema de ecuaciones",    "value": "ec-system"},
                ],
                value="matrix_operations",
                className="radio-group",
                inline=True,
            ),
        ]),

        # ───────────────────────────────────────────────
        # Selector de método
        # ───────────────────────────────────────────────
        html.Div(className="card", children=[
            html.Label("Método"),
            dcc.Dropdown(
                id="la-calculation-mode",
                options=[
                    # Matrix operations
                    {"label": "Determinante",        "value": "determinant"},
                    {"label": "Inversa",             "value": "inverse"},
                    {"label": "Norma",               "value": "norm"},
                    {"label": "Número de condición", "value": "condition_number"},
                    {"label": "Transpuesta",         "value": "transpose"},
                    {"label": "Rango",               "value": "rank"},

                    # System solvers
                    {"label": "Gauss",               "value": "gauss"},
                    {"label": "Gauss-Jordan",        "value": "gauss_jordan"},
                    {"label": "LU",                  "value": "lu"},
                    {"label": "Cholesky",            "value": "cholesky"},
                    {"label": "QR",                  "value": "qr"},
                    {"label": "Jacobi",              "value": "jacobi"},
                    {"label": "Gauss-Seidel",        "value": "gauss_seidel"},
                ],
                placeholder="Selecciona un método",
                className="input",
            ),
        ]),

        # ───────────────────────────────────────────────
        # Área de modo de entrada (SIEMPRE presente)
        # ───────────────────────────────────────────────
        html.Div(className="card", id="la-mode-area", children=[

            # Selector de modo
            html.Label("Modo de entrada"),
            dcc.RadioItems(
                id="la-input-mode",
                options=[
                    {"label": "Subir archivo", "value": "upload"},
                    {"label": "Tabla manual",  "value": "table"},
                ],
                value="upload",
                className="radio-group",
                inline=True,
            ),

            # Upload (visible por default)
            html.Div(
                id="la-upload-area",
                children=[
                    dcc.Upload(
                        id="la-upload",
                        children=html.Div(["Arrastra o ", html.A("selecciona un archivo")]),
                        className="upload-area",
                        accept=".txt,.csv,.xlsx",
                    ),
                    html.Div(id="la-upload-preview"),
                ],
                hidden=False,
            ),

            # Tabla (oculta por default)
            html.Div(
                id="la-table-area",
                hidden=True,
                children=[
                    html.Label("Matriz A"),
                    dash_table.DataTable(
                        id="la-table-A",
                        columns=[{"name": f"col{i}", "id": f"col{i}", "editable": True} for i in range(3)],
                        data=[{f"col{i}": "" for i in range(3)} for _ in range(3)],
                        editable=True,
                        row_deletable=True,
                    ),
                    html.Br(),
                    html.Label("Vector b (solo para sistemas)"),
                    dcc.Input(
                        id="la-vector-b",
                        type="text",
                        placeholder="ej: 1 2 3",
                        className="input",
                    ),
                ],
            ),
        ]),

        # ───────────────────────────────────────────────
        # Botón de ejecución
        # ───────────────────────────────────────────────
        html.Div(className="card", id="la-btn-card", children=[
            html.Button("Calcular", id="la-run-btn", className="btn-primary"),
        ]),

        # ───────────────────────────────────────────────
        # Área de resultados
        # ───────────────────────────────────────────────
        html.Div(
            id="linear-algebra-result-area",
            className="result-area"
        ),
    ],
)
