from dash import html, dcc, dash_table
from core.ui.styled_components import (
    styled_dropdown,
    styled_radioitems,
    styled_input,
    styled_button
)
from core.ui.tooltips import Tooltip
from app.tooltips import get_tooltip

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
        html.Div(className="module-card", children=[
            html.Div(className="label-with-tooltip", children=[
                html.Div("Tipo de operación", className="na-label"),
                Tooltip(get_tooltip("la-calculation-type")).render()
            ]),
            styled_radioitems(
                id="la-calculation-type",
                options=[
                    {"label": "Operaciones con matrices", "value": "matrix_operations"},
                    {"label": "Sistema de ecuaciones",    "value": "ec-system"},
                ],
                value="matrix_operations",
            ),
        ]),

        # ───────────────────────────────────────────────
        # Selector de método
        # ───────────────────────────────────────────────
        html.Div(className="module-card", children=[
            html.Div(className="label-with-tooltip", children=[
                html.Div("Método", className="na-label"),
                Tooltip(get_tooltip("la-calculation-mode")).render()
            ]),
            styled_dropdown(
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
            ),
        ]),

        # ───────────────────────────────────────────────
        # Área de modo de entrada
        # ───────────────────────────────────────────────
        html.Div(className="module-card", id="la-mode-area", children=[

            html.Div(className="label-with-tooltip", children=[
                html.Div("Modo de Entrada", className="na-label"),
                Tooltip(get_tooltip("la-input-mode")).render()
            ]),
            styled_radioitems(
                id="la-input-mode",
                options=[
                    {"label": "Subir archivo", "value": "upload"},
                    {"label": "Tabla manual",  "value": "table"},
                ],
                value="upload",
            ),

            # ─────────────────────────────────────────────
            # Upload (visible por default)
            # ─────────────────────────────────────────────
            html.Div(
                id="la-upload-area",
                hidden=False,
                children=[
                    html.Div(className="label-with-tooltip", children=[
                        html.Div("Upload", className="na-label"),
                        Tooltip(get_tooltip("la-upload")).render()
                    ]),
                    dcc.Upload(
                        id="la-upload",
                        children=html.Div(["Arrastra o ", html.A("selecciona un archivo")]),
                        className="upload-area",
                        accept=".txt,.csv,.xlsx",
                    ),
                    html.Div(id="la-upload-preview"),
                ],
            ),

            # ─────────────────────────────────────────────
            # Tabla manual (oculta por default)
            # ─────────────────────────────────────────────
            html.Div(
                id="la-table-area",
                hidden=True,
                children=[
                    html.Div(className="label-with-tooltip", children=[
                        html.Div("Matriz A", className="na-label"),
                        Tooltip(get_tooltip("la-table-A")).render()
                    ]),
                    dash_table.DataTable(
                        id="la-table-A",
                        columns=[{"name": f"col{i}", "id": f"col{i}", "editable": True} for i in range(3)],
                        data=[{f"col{i}": "" for i in range(3)} for _ in range(3)],
                        editable=True,
                        row_deletable=True,
                    ),

                    html.Br(),

                    html.Div(id="la-vector-b-area", children=[
                        html.Div(className="label-with-tooltip", children=[
                            html.Div("Vector b (solo para sistemas)", className="na-label"),
                            Tooltip(get_tooltip("la-vector-b")).render()
                        ]),
                        styled_input(
                            id="la-vector-b",
                            type="text",
                            placeholder="ej: 1 2 3",
                        ),
                    ]),
                ],
            ),
        ]),

        # ───────────────────────────────────────────────
        # Botón de ejecución
        # ───────────────────────────────────────────────
        html.Div(className="module-card", id="la-btn-card", children=[
            Tooltip(get_tooltip("la-run-btn")).render(),
            styled_button(
                id="la-run-btn",
                label="Calcular",
                kind="primary",
            ),
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
