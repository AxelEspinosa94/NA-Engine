from dash import html, dcc
from core.ui.styled_components import (
    styled_dropdown,
    styled_radioitems,
    styled_input,
    styled_button
)

from core.ui.tooltips import Tooltip
from app.tooltips import get_tooltip
from typing import List, Dict, Any

# ───────────────────────────────────────────────
# Modo de entrada (siempre función)
# ───────────────────────────────────────────────
def integr_input_mode(options: List[Dict] = None):
    return html.Div(className="module-card", id="integr-mode-card", children=[
        html.Div(className="label-with-tooltip", children=[
            html.Div("Input Type", className="na-label"),
            Tooltip(get_tooltip("integr-input-mode")).render()
        ]),
        styled_radioitems(
            id="integr-input-mode",
            options=options,
            value="function",
        ),
    ])