from dash import html, dcc


interpolation_section = html.Div(
    id="interpolation-container",
    children=[

        html.Div(
            className="module-header",
            children=[
                html.H2("Interpolación Numérica"),
                html.P("Métodos de Newton, Lagrange y Splines Cúbicos."),
            ],
        ),

        # Selector de método
        html.Div(
            className="card",
            children=[
                html.Label("Selecciona el método"),
                dcc.Dropdown(
                    id="interp-method",
                    options=[
                        {"label": "Newton", "value": "newton"},
                        {"label": "Lagrange", "value": "lagrange"},
                        {"label": "Splines Cúbicos", "value": "splines"},
                    ],
                    placeholder="Selecciona un método",
                    className="input",
                ),
            ],
        ),

        # Área dinámica
        html.Div(id="interp-dynamic-area", className="card"),

    ],
)
