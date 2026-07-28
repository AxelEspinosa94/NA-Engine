from dash import html, dcc
from core.ui.styled_components import (
    styled_dropdown,
    styled_radioitems,
    styled_input,
    styled_button
)
from core.ui.tooltips import Tooltip
from app.tooltips import get_tooltip

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
        html.Div(className="module-card", children=[
            html.Div(className="label-with-tooltip", children=[
                html.Div("Método", className="na-label"),
                Tooltip(get_tooltip("integr-method")).render()
            ]),
            styled_dropdown(
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
            ),
        ]),

        # ───────────────────────────────────────────────
        # Modo de entrada (siempre función)
        # ───────────────────────────────────────────────
        html.Div(className="module-card", id="integr-mode-card", children=[
            html.Div(className="label-with-tooltip", children=[
                html.Div("Modo de Entrada", className="na-label"),
                Tooltip(get_tooltip("integr-input-mode")).render()
            ]),
            styled_radioitems(
                id="integr-input-mode",
                options=[{"label": "Función f(x)", "value": "function"}],
                value="function",
            ),
        ]),

        # ───────────────────────────────────────────────
        # Área dinámica de input (contenedores predefinidos)
        # ───────────────────────────────────────────────
        html.Div(id="integr-input-area", className="module-card input-area", children=[

            # ─────────────────────────────────────────────
            # MODO: función f(x)
            # ─────────────────────────────────────────────
            html.Div(id="integr-mode-function", hidden=True, children=[
                html.Div(className="label-with-tooltip", children=[
                    html.Div("Función f(x)", className="na-label"),
                    Tooltip(get_tooltip("integr-fn")).render()
                ]),
                styled_input(
                    id="integr-fn",
                    type="text",
                    placeholder="ej: sin(x) + x**2",
                ),

                html.Label("Intervalo [a, b]"),
                html.Div(className="input-row", children=[
                    html.Div(className="label-with-tooltip", children=[
                        html.Div("a", className="na-label"),
                        Tooltip(get_tooltip("integr-a")).render()
                    ]),
                    styled_input(id="integr-a", type="number", placeholder="a"),
                    html.Div(className="label-with-tooltip", children=[
                        html.Div("b", className="na-label"),
                        Tooltip(get_tooltip("integr-b")).render()
                    ]),
                    styled_input(id="integr-b", type="number", placeholder="b"),
                ]),

                html.Div(className="label-with-tooltip", children=[
                    html.Div("Número de subintervalos (n)", className="na-label"),
                    Tooltip(get_tooltip("integr-n")).render()
                ]),
                styled_input(
                    id="integr-n",
                    type="number",
                    placeholder="ej: 10",
                ),
            ]),

            # ─────────────────────────────────────────────
            # MODO: Gauss-Legendre (solo puntos)
            # ─────────────────────────────────────────────
            html.Div(id="integr-mode-gauss", hidden=True, children=[
                html.Div(className="label-with-tooltip", children=[
                    html.Div("Puntos de Gauss-Legendre", className="na-label"),
                    Tooltip(get_tooltip("integr-gauss-points")).render()
                ]),
                styled_input(
                    id="integr-gauss-points",
                    type="number",
                    placeholder="ej: 2",
                ),
            ]),
        ]),

        # ───────────────────────────────────────────────
        # Botón de ejecución
        # ───────────────────────────────────────────────
        html.Div(className="module-card", id="integr-btn-card", hidden=True, children=[
            Tooltip(get_tooltip("integr-run-btn")).render(),
            styled_button("integr-run-btn", "Calcular"),
        ]),

        # ───────────────────────────────────────────────
        # Área de resultados
        # ───────────────────────────────────────────────
        html.Div(id="integr-result-area", className="result-area"),
    ],
)
