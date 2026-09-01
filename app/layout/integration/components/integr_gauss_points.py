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
# MODO: Gauss-Legendre (solo puntos)
# ───────────────────────────────────────────────
def integr_gauss_points():
    return html.Div(
        id="integr-mode-gauss",
        hidden=True,
        children=[
            html.Div(
                className="label-with-tooltip",
                children=[
                    html.Div("Gauss-Legendre Points", className="na-label"),
                    Tooltip(get_tooltip("integr-gauss-points")).render(),
                ],
            ),
            styled_input(
                id="integr-gauss-points",
                type="number",
                placeholder="ej: 2",
            ),
        ],
    )
