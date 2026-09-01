from dash import dcc, html

from app.tooltips import get_tooltip
from core.ui.styled_components import (
    styled_button,
    styled_dropdown,
    styled_input,
    styled_radioitems,
)
from core.ui.tooltips import Tooltip


# ───────────────────────────────────────────────
# Área dinámica de input (contenedores predefinidos)
# ───────────────────────────────────────────────
def integr_input_area():
    return html.Div(
        id="integr-input-area",
        className="module-card input-area",
        children=[
            # ─────────────────────────────────────────────
            # MODO: función f(x)
            # ─────────────────────────────────────────────
            html.Div(
                id="integr-mode-function",
                hidden=True,
                children=[
                    html.Div(
                        className="label-with-tooltip",
                        children=[
                            html.Div("Function f(x)", className="na-label"),
                            Tooltip(get_tooltip("integr-fn")).render(),
                        ],
                    ),
                    styled_input(
                        id="integr-fn",
                        type="text",
                        placeholder="ex: sin(x) + x**2",
                    ),
                    html.Label("Interval [a, b]"),
                    html.Div(
                        className="input-row",
                        children=[
                            html.Div(
                                className="label-with-tooltip",
                                children=[
                                    html.Div("a", className="na-label"),
                                    Tooltip(get_tooltip("integr-a")).render(),
                                ],
                            ),
                            styled_input(id="integr-a", type="number", placeholder="a"),
                            html.Div(
                                className="label-with-tooltip",
                                children=[
                                    html.Div("b", className="na-label"),
                                    Tooltip(get_tooltip("integr-b")).render(),
                                ],
                            ),
                            styled_input(id="integr-b", type="number", placeholder="b"),
                        ],
                    ),
                    html.Div(
                        className="label-with-tooltip",
                        children=[
                            html.Div(
                                "Number of Subintervals (n)", className="na-label"
                            ),
                            Tooltip(get_tooltip("integr-n")).render(),
                        ],
                    ),
                    styled_input(
                        id="integr-n",
                        type="number",
                        placeholder="ej: 10",
                    ),
                ],
            )
        ],
    )
