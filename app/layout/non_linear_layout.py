from dash import dcc, html

from app.tooltips import get_tooltip
from core.ui.styled_components import (
    styled_button,
    styled_dropdown,
    styled_input,
    styled_radioitems,
)
from core.ui.tooltips import Tooltip

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
                html.P(
                    "Métodos de Bisección, Falsa Posición, Secante, Newton y Punto Fijo."
                ),
            ],
        ),
        # ───────────────────────────────────────────────
        # Selector de método
        # ───────────────────────────────────────────────
        html.Div(
            className="module-card",
            children=[
                html.Div(
                    className="label-with-tooltip",
                    children=[
                        html.Div("Método", className="na-label"),
                        Tooltip(get_tooltip("nonlin-method")).render(),
                    ],
                ),
                styled_dropdown(
                    id="nonlin-method",
                    options=[
                        {"label": "Bisección", "value": "bisection"},
                        {"label": "Falsa Posición", "value": "false_position"},
                        {"label": "Newton", "value": "newton"},
                        {"label": "Secante", "value": "secant"},
                        {"label": "Punto Fijo", "value": "fixed_point"},
                    ],
                    placeholder="Selecciona un método",
                ),
            ],
        ),
        # ───────────────────────────────────────────────
        # Modo de entrada (siempre función)
        # ───────────────────────────────────────────────
        html.Div(
            className="module-card",
            id="nonlin-mode-card",
            children=[
                html.Div(
                    className="label-with-tooltip",
                    children=[
                        html.Div("Modo de entrada", className="na-label"),
                        Tooltip(get_tooltip("nonlin-input-mode")).render(),
                    ],
                ),
                styled_radioitems(
                    id="nonlin-input-mode",
                    options=[{"label": "Función f(x)", "value": "function"}],
                    value="function",
                ),
            ],
        ),
        # ───────────────────────────────────────────────
        # Área dinámica de input (contenedores predefinidos)
        # ───────────────────────────────────────────────
        html.Div(
            id="nonlin-input-area",
            className="module-card input-area",
            children=[
                # ─────────────────────────────────────────────
                # Función f(x)
                # ─────────────────────────────────────────────
                html.Div(
                    id="nonlin-mode-base",
                    hidden=True,
                    children=[
                        html.Div(
                            className="label-with-tooltip",
                            children=[
                                html.Div("Función f(x)", className="na-label"),
                                Tooltip(get_tooltip("nonlin-f")).render(),
                            ],
                        ),
                        styled_input(
                            id="nonlin-f",
                            type="text",
                            placeholder="ej: x**2 - 5",
                        ),
                        html.Div(
                            className="label-with-tooltip",
                            children=[
                                html.Div("Valor inicial x0", className="na-label"),
                                Tooltip(get_tooltip("nonlin-x0")).render(),
                            ],
                        ),
                        styled_input(
                            id="nonlin-x0",
                            type="number",
                            placeholder="ej: 2.0",
                        ),
                    ],
                ),
                # ─────────────────────────────────────────────
                # g(x) — solo para punto fijo
                # ─────────────────────────────────────────────
                html.Div(
                    id="nonlin-mode-g",
                    hidden=True,
                    children=[
                        html.Div(
                            className="label-with-tooltip",
                            children=[
                                html.Div("Función g(x)", className="na-label"),
                                Tooltip(get_tooltip("nonlin-g")).render(),
                            ],
                        ),
                        styled_input(
                            id="nonlin-g",
                            type="text",
                            placeholder="ej: 0.5*(x + 5/x)",
                        ),
                    ],
                ),
                # ─────────────────────────────────────────────
                # x1 — solo para secante
                # ─────────────────────────────────────────────
                html.Div(
                    id="nonlin-mode-x1",
                    hidden=True,
                    children=[
                        html.Div(
                            className="label-with-tooltip",
                            children=[
                                html.Div("Valor inicial x1", className="na-label"),
                                Tooltip(get_tooltip("nonlin-x1")).render(),
                            ],
                        ),
                        styled_input(
                            id="nonlin-x1",
                            type="number",
                            placeholder="ej: 3.0",
                        ),
                    ],
                ),
                # ─────────────────────────────────────────────
                # Intervalo [a, b] — bisección y falsa posición
                # ─────────────────────────────────────────────
                html.Div(
                    id="nonlin-mode-interval",
                    hidden=True,
                    children=[
                        html.Div(
                            className="label-with-tooltip",
                            children=[
                                html.Div("Intervalo [a, b]", className="na-label"),
                                Tooltip(get_tooltip("nonlin-interval")).render(),
                            ],
                        ),
                        html.Br(),
                        html.Div(
                            className="input-row",
                            children=[
                                html.Div(
                                    className="label-with-tooltip",
                                    children=[
                                        html.Div(
                                            "Extremo izquierdo a", className="na-label"
                                        ),
                                        Tooltip(get_tooltip("nonlin-a")).render(),
                                    ],
                                ),
                                styled_input(
                                    id="nonlin-a", type="number", placeholder="a"
                                ),
                                html.Div(
                                    className="label-with-tooltip",
                                    children=[
                                        html.Div(
                                            "Extremo derecho b", className="na-label"
                                        ),
                                        Tooltip(get_tooltip("nonlin-b")).render(),
                                    ],
                                ),
                                styled_input(
                                    id="nonlin-b", type="number", placeholder="b"
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
        # ───────────────────────────────────────────────
        # Botón de ejecución
        # ───────────────────────────────────────────────
        html.Div(
            className="module-card",
            id="nonlin-btn-card",
            hidden=True,
            children=[
                Tooltip(get_tooltip("nonlin-run-btn")).render(),
                styled_button(
                    id="nonlin-run-btn",
                    label="Calcular",
                    kind="primary",
                ),
            ],
        ),
        # ───────────────────────────────────────────────
        # Área de resultados
        # ───────────────────────────────────────────────
        html.Div(id="nonlin-result-area", className="result-area"),
    ],
)
