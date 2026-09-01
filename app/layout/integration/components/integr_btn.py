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
# Selector de método
# ───────────────────────────────────────────────
def integr_run_btn():
    return html.Div(
        className="module-card",
        id="integr-btn-card",
        hidden=True,
        children=[
            Tooltip(get_tooltip("integr-run-btn")).render(),
            styled_button("integr-run-btn", "Calcular"),
        ],
    )
