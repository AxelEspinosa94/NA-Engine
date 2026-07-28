from dash import html, dcc
from core.ui.styled_components import (
    styled_dropdown,
    styled_radioitems,
    styled_input,
    styled_button,
    styled_textarea
)
from core.ui.tooltips import Tooltip
from app.tooltips import get_tooltip


ode_section = html.Div(
    id="ode-container",
    children=[

        # ───────────────────────────────────────────────
        # Encabezado del módulo
        # ───────────────────────────────────────────────
        html.Div(
            className="module-header",
            children=[
                html.H2("Ecuaciones Diferenciales Ordinarias (ODE)"),
                html.P("Métodos IVP, sistemas, shooting y diferencias finitas."),
            ],
        ),

        # ───────────────────────────────────────────────
        # Selector de método
        # ───────────────────────────────────────────────
        html.Div(className="module-card", children=[
            html.Div(className="label-with-tooltip", children=[
                html.Div("Método", className="na-label"),
                Tooltip(get_tooltip("ode-method")).render()
            ]),
            styled_dropdown(
                id="ode-method",
                options=[
                    {"label": "Euler",                 "value": "euler"},
                    {"label": "Heun",                  "value": "heun"},
                    {"label": "Runge–Kutta 2",         "value": "rk2"},
                    {"label": "Runge–Kutta 4",         "value": "rk4"},
                    {"label": "RK4 Sistema",           "value": "rk4_system"},
                    {"label": "Shooting (BVP)",        "value": "shooting"},
                    {"label": "Diferencias Finitas",   "value": "finite_differences"},
                    {"label": "Adams–Bashforth 2",     "value": "adams_bashforth_2"},
                    {"label": "Adams–Bashforth 3",     "value": "adams_bashforth_3"},
                    {"label": "Adams–Moulton 2",       "value": "adams_moulton_2"},
                ],
                placeholder="Selecciona un método",
            ),
        ]),

        # ───────────────────────────────────────────────
        # Selector de modo de entrada
        # ───────────────────────────────────────────────
        html.Div(className="module-card", children=[
            html.Div(className="label-with-tooltip", children=[
                            html.Div("Modo de entrada", className="na-label"),
                            Tooltip(get_tooltip("ode-input-mode")).render()
                        ]),
            styled_radioitems(
                id="ode-input-mode",
                options=[
                    {"label": "Función f(x, y)", "value": "function"},
                    {"label": "Sistema",         "value": "system"},
                ],
                value="function",
            ),
        ]),

        # ───────────────────────────────────────────────
        # Área dinámica de input (función o sistema)
        # ───────────────────────────────────────────────
        html.Div(id="ode-input-area", className="module-card input-area", children=[

            # Función f(x, y)
            html.Div(id="ode-function-card", hidden=False, children=[
                html.Div(className="label-with-tooltip", children=[
                                html.Div("f(x, y)", className="na-label"),
                                Tooltip(get_tooltip("ode-function")).render()
                            ]),
                styled_input(
                    id="ode-function",
                    type="text",
                    placeholder="Ej: x + y",
                ),
            ]),

            # Sistema de ecuaciones
            html.Div(id="ode-system-card", hidden=True, children=[
                html.Div(className="label-with-tooltip", children=[
                                html.Div("Sistema de ecuaciones", className="na-label"),
                                Tooltip(get_tooltip("ode-system")).render()
                            ]),
                styled_textarea(
                    id="ode-system",
                    placeholder="Ej:\ny1' = y2\ny2' = -y1",
                ),
            ]),
        ]),

        # ───────────────────────────────────────────────
        # Campos IVP
        # ───────────────────────────────────────────────
        html.Div(id="ode-ivp-card", className="module-card", hidden=True, children=[
            html.Div(className="label-with-tooltip", children=[
                    html.Div("Condiciones Iniciales", className="na-label"),
                    Tooltip(get_tooltip("ode-ivp")).render()
            ]),
            html.Div(className="input-row", children=[
                html.Div(children=[
                    html.Div(className="label-with-tooltip", children=[
                        html.Div("x₀", className="na-label"),
                        Tooltip(get_tooltip("ode-x0")).render()
                    ]),
                    styled_input(id="ode-x0", type="number"),
                ]),
                html.Div(children=[
                    html.Div(className="label-with-tooltip", children=[
                        html.Div("y₀", className="na-label"),
                        Tooltip(get_tooltip("ode-y0")).render()
                    ]),
                    styled_input(id="ode-y0", type="number"),
                ]),
                html.Div(children=[
                    html.Div(className="label-with-tooltip", children=[
                        html.Div("x final", className="na-label"),
                        Tooltip(get_tooltip("ode-x-end")).render()
                    ]),
                    styled_input(id="ode-x-end", type="number"),
                ]),
                html.Div(children=[

                    html.Div(className="label-with-tooltip", children=[
                        html.Div("Paso h", className="na-label"),
                        Tooltip(get_tooltip("ode-h")).render()
                    ]),
                    styled_input(id="ode-h", type="number"),
                ]),
            ]),
        ]),

        # ───────────────────────────────────────────────
        # Campos para sistemas (vector y0)
        # ───────────────────────────────────────────────
        html.Div(id="ode-system-y0-card", className="module-card", hidden=True, children=[
            html.Div(className="label-with-tooltip", children=[
                html.Div("Vector inicial y₀", className="na-label"),
                Tooltip(get_tooltip("ode-y0-system")).render()
            ]),
            styled_textarea(
                id="ode-y0-system",
                placeholder="Ej: 1, 0, -2",
            ),
        ]),

        # ───────────────────────────────────────────────
        # Campos BVP — Shooting
        # ───────────────────────────────────────────────
        html.Div(id="ode-shooting-card", className="module-card", hidden=True, children=[
            html.Div(className="label-with-tooltip", children=[
                html.Div("Condiciones de frontera (Shooting)", className="na-label"),
                Tooltip(get_tooltip("ode-shooting")).render()
            ]),
            html.Div(className="input-row", children=[
                html.Div(children=[
                    html.Div(className="label-with-tooltip", children=[
                        html.Div("α = y(x₀)", className="na-label"),
                        Tooltip(get_tooltip("ode-alpha")).render(),
                    ]),
                    styled_input(id="ode-alpha", type="number"),
                ]),
                html.Div(children=[
                    html.Div(className="label-with-tooltip", children=[
                        html.Div("β = y(x_end)", className="na-label"),
                        Tooltip(get_tooltip("ode-beta")).render()
                    ]),
                    styled_input(id="ode-beta", type="number"),
                ]),
                html.Div(children=[
                    html.Div(className="label-with-tooltip", children=[
                        html.Div("Pendiente inicial s₀", className="na-label"),
                        Tooltip(get_tooltip("ode-s0")).render()
                    ]),
                    styled_input(id="ode-s0", type="number"),
                ]),
            ]),
        ]),

        # ───────────────────────────────────────────────
        # Campos BVP — Diferencias finitas
        # ───────────────────────────────────────────────
        html.Div(id="ode-fd-card", className="module-card", hidden=True, children=[
            html.Div(className="label-with-tooltip", children=[
                html.Div("Diferencias finitas", className="na-label"),
                Tooltip(get_tooltip("ode-fd")).render()
            ]),
            html.Div(className="input-row", children=[
                html.Div(children=[
                    html.Div(className="label-with-tooltip", children=[
                        html.Div("α = y(x₀)", className="na-label"),
                        Tooltip(get_tooltip("ode-alpha-fd")).render()
                    ]),
                    styled_input(id="ode-alpha-fd", type="number"),
                ]),
                html.Div(children=[
                    html.Div(className="label-with-tooltip", children=[
                        html.Div("β = y(x_end)", className="na-label"),
                        Tooltip(get_tooltip("ode-beta-fd")).render()
                    ]),
                    styled_input(id="ode-beta-fd", type="number"),
                ]),
                html.Div(children=[
                    html.Div(className="label-with-tooltip", children=[
                        html.Div("n (subdivisiones)", className="na-label"),
                        Tooltip(get_tooltip("ode-n")).render()
                    ]),
                    styled_input(id="ode-n", type="number"),
                ]),
            ]),
        ]),

        # ───────────────────────────────────────────────
        # Botón de ejecución
        # ───────────────────────────────────────────────
        html.Div(className="module-card", id="ode-btn-card", hidden=True, children=[
            Tooltip(get_tooltip("ode-run-btn")).render(),
            styled_button(
                id="ode-run-btn",
                label="Calcular",
                kind="primary",
            ),
        ]),

        # ───────────────────────────────────────────────
        # Área de resultados
        # ───────────────────────────────────────────────
        html.Div(id="ode-result-area", className="result-area"),
    ],
)
