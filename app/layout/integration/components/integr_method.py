from dash import html, dcc
from core.ui.styled_components import (
    styled_dropdown,
    styled_radioitems,
    styled_input,
    styled_button
)
from typing import List, Dict, Any
from core.ui.tooltips import Tooltip
from app.tooltips import get_tooltip

# ───────────────────────────────────────────────
# Selector de método
# ───────────────────────────────────────────────
def integr_method(options: List[Dict]=None):
    return html.Div(className="module-card", children=[
        html.Div(className="label-with-tooltip", children=[
            html.Div("Method", className="na-label"),
            Tooltip(get_tooltip("integr-method")).render()
        ]),
        styled_dropdown(
            id="integr-method",
            options=options,
            placeholder="Selecciona un método",
        ),
    ])