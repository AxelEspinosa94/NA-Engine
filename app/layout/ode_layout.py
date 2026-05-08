from dash import html, dcc
import app_deuteros_contents as contents


ode_section = html.Div(
    id="ode-container",
    children=[

        html.Div(
            className="module-header",
            children=[
                html.H2("Punto Fijo y Ecuaciones Diferenciales"),
                html.P("Método del Punto Fijo, Euler, Runge–Kutta y más."),
            ],
        ),

        html.Div(
            className="card",
            children=[
                html.Label("Selecciona el método"),
                dcc.Dropdown(
                    id="ode-method",
                    options=[
                        {"label": "Punto Fijo", "value": "fixed_point"},
                        {"label": "Euler", "value": "euler"},
                        {"label": "Runge–Kutta 4", "value": "rk4"},
                    ],
                    placeholder="Selecciona un método",
                    className="input",
                ),
            ],
        ),

        html.Div(id="ode-dynamic-area", className="card"),

    ],
)
