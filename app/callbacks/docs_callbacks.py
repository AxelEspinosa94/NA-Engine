# callbacks/docs_callbacks.py

import os
import markdown
from dash import Input, Output, State, dcc
from dash import no_update

def register_docs_callbacks(app):

    @app.callback(
        Output("docs-method", "options"),
        Input("docs-module", "value"),
    )
    def load_methods(module):

        if module is None:
            return []

        mapping = {
            "numerical_derivative": [
                {"label": "Forward", "value": "forward-derivative"},
                {"label": "Backward", "value": "backward-derivative"},
                {"label": "Central", "value": "central-derivative"},
                {"label": "Richardson", "value": "richardson"},
                {"label": "Partial Derivatives", "value": "partial-derivatives"},
                {"label": "Second Derivative", "value": "second-derivative"},
                {"label": "Third Derivative", "value": "third-derivative"},
            ],
            "integration": [
                {"label": "Trapezoid", "value": "trapezoid"},
                {"label": "Simpson", "value": "simpson"},
                {"label": "Romberg", "value": "romberg"},
                {"label": "Gauss-Legendre", "value": "gauss-legendre"},
            ],
            "interpolation": [
                {"label": "Lagrange", "value": "lagrange"},
                {"label": "Newton", "value": "newton"},
                {"label": "Hermite", "value": "hermite"},
                {"label": "Splines", "value": "spline_cubic"},
            ],
            "linear_algebra": [
                # Matrix operations
                {"label": "Determinant",        "value": "determinant"},
                {"label": "Inverse",             "value": "inverse"},
                {"label": "Norm",               "value": "norm"},
                {"label": "Condition Number", "value": "condition-number"},
                {"label": "Transpose",         "value": "transpose"},
                {"label": "Rank",               "value": "rank"},

                # System solvers
                {"label": "Gauss",               "value": "gauss"},
                {"label": "Gauss-Jordan",        "value": "gauss-jordan"},
                {"label": "LU",                  "value": "lu"},
                {"label": "Cholesky",            "value": "cholesky"},
                {"label": "QR",                  "value": "qr"},
                {"label": "Jacobi",              "value": "jacobi"},
                {"label": "Gauss-Seidel",        "value": "gauss-seidel"},
            ],
            "nonlinear": [
                {"label": "Bisection",        "value": "bisection"},
                {"label": "Regula Falsi",  "value": "false_position"},
                {"label": "Newton-Raphson",          "value": "newton-raphson"},
                {"label": "Secant",         "value": "secant"},
                {"label": "Fixed Point",      "value": "fixed_point"},
            ],
            "ode": [
                {"label": "Euler", "value": "euler"},
                {"label": "Heun", "value": "heun"},
                {"label": "RK2", "value": "rk2"},
                {"label": "RK4", "value": "rk4"},
                {"label": "RK4 Sistema", "value": "rk4-system"},
                {"label": "Shooting", "value": "shooting"},
                {"label": "Diferencias Finitas", "value": "finite-differences-bvp"},
                {"label": "Adams–Bashforth", "value": "adams-bashforth"},
                {"label": "Adams–Moulton 2", "value": "adams-moulton-2"},
            ],
        }

        return mapping.get(module, [])

    @app.callback(
        Output("docs-btn-card", "hidden"),
        Input("docs-method", "value"),
    )
    def show_button(method):
        return method is None

    @app.callback(
        Output("docs-result-area", "children"),
        Input("docs-run-btn", "n_clicks"),
        State("docs-module", "value"),
        State("docs-method", "value"),
        prevent_initial_call=True,
    )
    def render_docs(n_clicks, module, method):

        md_path = f"docs/theory/{module}/theory_{method}.md"

        with open(md_path, "r", encoding="utf-8") as f:
            raw_md = f.read()

        # Inyectar HTML crudo (MathJax lo detecta)
        return dcc.Markdown(
            children=raw_md, className="markdown-doc", mathjax=True)

