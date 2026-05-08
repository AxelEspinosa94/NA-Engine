from dash import html, dcc
import app_deuteros_contents as contents


integration_section = html.Div(
    id="integration-container",
    children=[

        html.Div(
            className="module-header",
            children=[
                html.H2("Integración Numérica"),
                html.P("Métodos de Simpson, Trapecio y combinaciones."),
            ],
        ),

        html.Div(
            className="card",
            children=[
                html.Label("Selecciona el método"),
                dcc.Dropdown(
                    id="integration-method",
                    options=[
                        {"label": "Regla de Simpson", "value": "simpson"},
                        {"label": "Regla del Trapecio", "value": "trapezoidal"},
                    ],
                    placeholder="Selecciona un método",
                    className="input",
                ),
            ],
        ),

        html.Div(id="integration-dynamic-area", className="card"),

    ],
)
