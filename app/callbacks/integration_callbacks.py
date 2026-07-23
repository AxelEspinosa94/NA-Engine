# app/callbacks/integration_callbacks.py

import pandas as pd
import numpy as np
from dash import Input, Output, State, callback, html, dcc
from dash import no_update

from core.base_method import NumericalMethod
from core.contract import UIContract
from core.exceptions import ValidationError, InputError


contract = UIContract()

# ============================================================
# Helpers
# ============================================================

def _build_function_dataframe(fn_expr: str, a: float, b: float, n: int) -> pd.DataFrame:
    """
    Construye un DataFrame evaluando f(x) en n+1 puntos entre [a, b].
    """
    if not fn_expr:
        raise InputError("Debes ingresar una función f(x).")

    if n <= 0:
        raise InputError("n debe ser un entero positivo.")

    xs = np.linspace(float(a), float(b), int(n) + 1)

    def safe_eval(expr, x):
        try:
            return float(eval(expr, {"__builtins__": {}}, {"x": x, "np": np}))
        except Exception as e:
            raise InputError(f"Error evaluando f(x): {e}")

    ys = [safe_eval(fn_expr, x) for x in xs]

    return pd.DataFrame({"x": xs, "y": ys})


def _build_mode_area():
    """
    Área dinámica para modo función (único modo soportado).
    """
    return [
        html.Label(className="input-label", children="Función f(x)"),
        dcc.Input(
            id="integr-fn",
            type="text",
            placeholder="ej: sin(x) + x**2",
            className="input"
        ),

        html.Label(className="input-label", children="Intervalo [a, b]"),
        html.Div(className="input-row", children=[
            dcc.Input(id="integr-a", type="number", placeholder="a", className="input"),
            dcc.Input(id="integr-b", type="number", placeholder="b", className="input"),
        ]),

        html.Label(className="input-label", children="Número de subintervalos (n)"),
        dcc.Input(
            id="integr-n",
            type="number",
            placeholder="ej: 10",
            className="input"
        ),
    ]

def register_integration_callbacks(app):

    # ============================================================
    # Callback 1: Construye el formulario dinámico
    # ============================================================
    @app.callback(
        Output("integr-input-area", "children"),
        Output("integr-gauss-card", "hidden"),
        Output("integr-btn-card", "hidden"),
        Input("integr-method", "value"),
        Input("integr-input-mode", "value"),
        prevent_initial_call=True,
    )
    def build_input_area(method, mode):

        if not method:
            return [], True, True, True

        # Área dinámica (siempre función)
        area = _build_mode_area()

        # Gauss-Legendre requiere puntos
        gauss_hidden = method != "gauss"

        # Botón visible
        btn_hidden = False

        return area, gauss_hidden, btn_hidden

    # ============================================================
    # Callback 2: Ejecuta el cálculo
    # ============================================================
    @app.callback(
        Output("integr-result-area", "children"),
        Input("integr-run-btn", "n_clicks"),
        State("integr-method", "value"),
        State("integr-input-mode", "value"),
        State("integr-fn", "value"),
        State("integr-a", "value"),
        State("integr-b", "value"),
        State("integr-n", "value"),
        State("integr-gauss-points", "value"),
        prevent_initial_call=True,
    )
    def run_integration(n_clicks, method, mode, fn_expr, a, b, n, gauss_points):

        if not method or not fn_expr or a is None or b is None or n is None:
            return no_update

        # Construir DataFrame desde función
        try:
            df = _build_function_dataframe(fn_expr, a, b, n)
        except Exception as e:
            return contract.resolve(method, {
                "status":     "error",
                "error_type": "InputError",
                "message":    str(e),
                "context":    {},
            })

        # Construir input_data para NumericalMethod
        input_data = {
            "mode": "function",
            "function": fn_expr,
            "interval": [float(a), float(b)],
            "n": int(n),
            "calculation_mode": method,
        }

        if method == "gauss":
            input_data["gauss_points"] = int(gauss_points or 2)

        # Validación
        try:
            nm = NumericalMethod("integration", input_data)
            nm.validate_input()
        except Exception as e:
            return contract.resolve(method, {
                "status":     "error",
                "error_type": "ValidationError",
                "message":    str(e),
                "context":    input_data,
            })

        # Ejecución
        outcome = nm.execute()
        return contract.resolve(method, outcome)
