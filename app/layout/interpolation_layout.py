from core.ui.styled_components import (
    styled_dropdown,
    styled_radioitems,
    styled_input,
    styled_button
)
from dash import html, dcc
from dash import dash_table
from core.ui.tooltips import Tooltip
from app.tooltips import get_tooltip

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

        # Selector de método
        html.Div(className="module-card", children=[
            html.Div(className="label-with-tooltip", children=[
                html.Div("Método", className="na-label"),
                Tooltip(get_tooltip("interp-method")).render()
            ]),
            styled_dropdown(
                id="interp-method",
                options=[
                    {"label": "Lagrange", "value": "lagrange"},
                    {"label": "Newton", "value": "newton"},
                    {"label": "Hermite", "value": "hermite"},
                    {"label": "Splines Cúbicos", "value": "spline_cubic"},
                ],
                placeholder="Selecciona un método",
            ),
        ]),

        # Selector de modo
        html.Div(className="module-card", id="interp-mode-card", hidden=True, children=[
            html.Div(className="label-with-tooltip", children=[
                html.Div("Modo de entrada", className="na-label"),
                Tooltip(get_tooltip("interp-input-mode")).render()
            ]),
            styled_radioitems(
                id="interp-input-mode",
                options=[
                    {"label": "Función f(x)", "value": "function"},
                    {"label": "Tabla manual", "value": "table"},
                    {"label": "Subir archivo", "value": "upload"},
                ],
                value="table",
            ),
        ]),

        # ============================================================
        # ÁREA DINÁMICA — ahora con contenedores predefinidos
        # ============================================================
        html.Div(id="interp-input-area", className="module-card input-area", children=[

            # ─────────────────────────────────────────────
            # MODO: función f(x)
            # ─────────────────────────────────────────────
            html.Div(id="interp-mode-function", hidden=True, children=[
                html.Div(className="label-with-tooltip", children=[
                    html.Div("Función f(x)", className="na-label"),
                    Tooltip(get_tooltip("interp-fn")).render()
                ]),
                styled_input(
                    id="interp-fn",
                    type="text",
                    placeholder="ej: x**2 + 1",
                ),

                html.Label("Rango"),
                html.Div(className="input-row", children=[
                    html.Div(className="label-with-tooltip", children=[
                        html.Div("a", className="na-label"),
                        Tooltip(get_tooltip("interp-a")).render()
                    ]),
                    styled_input(id="interp-a", type="number", placeholder="a"),
                    html.Div(className="label-with-tooltip", children=[
                        html.Div("b", className="na-label"),
                        Tooltip(get_tooltip("interp-b")).render()
                    ]),
                    styled_input(id="interp-b", type="number", placeholder="b"),
                ]),

                html.Div(className="label-with-tooltip", children=[
                    html.Div("Número de puntos", className="na-label"),
                    Tooltip(get_tooltip("interp-n")).render()
                ]),
                styled_input(id="interp-n", type="number", placeholder="ej: 10"),
            ]),

            # ─────────────────────────────────────────────
            # MODO: subir archivo
            # ─────────────────────────────────────────────
            html.Div(id="interp-mode-upload", hidden=True, children=[
                html.Div(className="label-with-tooltip", children=[
                    html.Div("Upload", className="na-label"),
                    Tooltip(get_tooltip("interp-upload")).render()
                ]),
                dcc.Upload(
                    id="interp-upload",
                    children=html.Div(["Arrastra o ", html.A("selecciona un archivo")]),
                    className="upload-area",
                    accept=".csv,.txt",
                ),
                html.Div(id="interp-upload-preview"),
            ]),

            # ─────────────────────────────────────────────
            # MODO: tabla manual
            # ─────────────────────────────────────────────
            html.Div(id="interp-mode-table", hidden=True, children=[
                html.Div(className="label-with-tooltip", children=[
                    html.Div("Table", className="na-label"),
                    Tooltip(get_tooltip("interp-table")).render()
                ]),
                dash_table.DataTable(
                    id="interp-table",
                    columns=[{"name": c, "id": c, "editable": True} for c in ["x", "y"]],
                    data=[{"x": "", "y": ""} for _ in range(5)],
                    editable=True,
                    row_deletable=True,
                )
            ]),
        ]),

        # xk
        html.Div(className="module-card", id="interp-xk-card", hidden=True, children=[
            html.Div(className="label-with-tooltip", children=[
                html.Div("Valor a evaluar (xk)", className="na-label"),
                Tooltip(get_tooltip("interp-xk")).render()
            ]),
            styled_input(id="interp-xk", type="number", placeholder="ej: 1.5"),
        ]),

        # Botón
        html.Div(className="module-card", id="interp-btn-card", hidden=True, children=[
            Tooltip(get_tooltip("interp-run-btn")).render(),
            styled_button(id="interp-run-btn", label="Calcular"),
        ]),

        # Resultado
        html.Div(id="interp-result-area", className="result-area"),
    ],
)
