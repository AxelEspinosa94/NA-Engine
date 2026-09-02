from dash import html

from app.tooltips import get_tooltip
from core.ui.styled_components import (
    styled_button,
    styled_dropdown,
    styled_input,
    styled_radioitems,
)
from core.ui.tooltips import Tooltip

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
                html.P(
                    "Derivadas de primer, segundo y tercer orden, Richardson y parciales."
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
                        html.Div("Método de derivación", className="na-label"),
                        Tooltip(get_tooltip("deriv-method")).render(),
                    ],
                ),
                styled_dropdown(
                    id="deriv-method",
                    options=[
                        {"label": "Forward", "value": "forward"},
                        {"label": "Backward", "value": "backward"},
                        {"label": "Central", "value": "central"},
                        {"label": "Richardson", "value": "richardson"},
                        {"label": "2da Forward", "value": "second_forward"},
                        {"label": "2da Central", "value": "second_central"},
                        {"label": "3ra Forward", "value": "third_forward"},
                        {"label": "Parcial ∂/∂x", "value": "partial_x"},
                        {"label": "Parcial ∂/∂y", "value": "partial_y"},
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
            id="deriv-mode-card",
            children=[
                html.Div(
                    className="label-with-tooltip",
                    children=[
                        html.Div("Modo de entrada", className="na-label"),
                        Tooltip(get_tooltip("deriv-input-mode")).render(),
                    ],
                ),
                styled_radioitems(
                    id="deriv-input-mode",
                    options=[{"label": "Función f(x)", "value": "function"}],
                    value="function",
                ),
            ],
        ),
        # ───────────────────────────────────────────────
        # Área dinámica de input (contenedores predefinidos)
        # ───────────────────────────────────────────────
        html.Div(
            id="deriv-input-area",
            className="module-card input-area",
            children=[
                # ─────────────────────────────────────────────
                # Base: f(x), x, h
                # ─────────────────────────────────────────────
                html.Div(
                    id="deriv-mode-base",
                    hidden=True,
                    children=[
                        html.Div(
                            className="label-with-tooltip",
                            children=[
                                html.Div("Función f(x)", className="na-label"),
                                Tooltip(get_tooltip("deriv-function")).render(),
                            ],
                        ),
                        styled_input(
                            id="deriv-function",
                            type="text",
                            placeholder="ej: x**2 + 3*x",
                        ),
                        html.Div(
                            className="label-with-tooltip",
                            children=[
                                html.Div("Valor de x", className="na-label"),
                                Tooltip(get_tooltip("deriv-x")).render(),
                            ],
                        ),
                        styled_input(
                            id="deriv-x",
                            type="number",
                            placeholder="ej: 2.0",
                        ),
                        html.Div(
                            className="label-with-tooltip",
                            children=[
                                html.Div("Paso h", className="na-label"),
                                Tooltip(get_tooltip("deriv-h")).render(),
                            ],
                        ),
                        styled_input(
                            id="deriv-h",
                            type="number",
                            placeholder="ej: 0.01",
                        ),
                    ],
                ),
                # ───────────────────────────────────────────────
                # Input para y (solo visible en parciales)
                # ───────────────────────────────────────────────
                html.Div(
                    className="module-card",
                    id="deriv-y-card",
                    hidden=True,
                    children=[
                        html.Div(
                            className="label-with-tooltip",
                            children=[
                                html.Div("Valor de y", className="na-label"),
                                Tooltip(get_tooltip("deriv-y")).render(),
                            ],
                        ),
                        styled_input(
                            id="deriv-y",
                            type="number",
                            placeholder="ej: 3.0",
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
            id="deriv-btn-card",
            hidden=True,
            children=[
                Tooltip(get_tooltip("deriv-run-btn")).render(),
                styled_button(
                    id="deriv-run-btn",
                    label="Calcular",
                    kind="primary",
                ),
            ],
        ),
        # ───────────────────────────────────────────────
        # Área de resultados
        # ───────────────────────────────────────────────
        html.Div(id="deriv-result-area", className="result-area"),
    ],
)
