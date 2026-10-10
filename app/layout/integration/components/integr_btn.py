from dash import html

from app.tooltips import get_tooltip
from core.ui.styled_components import styled_button
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
