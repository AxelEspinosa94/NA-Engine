from dash import html, dcc
from core.ui.styled_components import (
    styled_dropdown,
    styled_radioitems,
    styled_input,
    styled_button
)

from core.ui.tooltips import Tooltip
from app.tooltips import get_tooltip

# ───────────────────────────────────────────────
# Selector de método
# ───────────────────────────────────────────────
def integr_run_btn():
    return html.Div(className="module-card", id="integr-btn-card", hidden=True, children=[
        Tooltip(get_tooltip("integr-run-btn")).render(),
        styled_button("integr-run-btn", "Calcular"),
    ])