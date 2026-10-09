from dash import dcc, html

from app.tooltips import get_tooltip
from core.ui.styled_components import styled_input
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
                    # dentro de integr_input_area(), reemplazando el bloque de a / b:
                    html.Label("Domain (one row per variable)"),
                    html.Div(id="integr-bounds-rows", children=[]),
                    html.Div(
                        className="input-row",
                        children=[
                            html.Button(
                                "+ dimension",
                                className="btn btn-secondary",
                                id="integr-add-dim",
                                n_clicks=0,
                            ),
                            html.Button(
                                "− dimension",
                                className="btn btn-secondary",
                                id="integr-remove-dim",
                                n_clicks=0,
                            ),
                        ],
                    ),
                    dcc.Store(id="integr-dim", data=1),
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
