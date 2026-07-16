# app/callbacks/nonlinear_callbacks.py

import pandas as pd
from dash import Input, Output, State, callback, html, dcc
from dash import no_update

from core.base_method import NumericalMethod
from core.contract import UIContract
from core.exceptions import ValidationError, InputError, ExecutionError

contract = UIContract()

# ============================================================
# Helpers
# ============================================================

def _build_base_area():
    """
    Área dinámica base: función f(x) y x0.
    """
    return [
        html.Label("Función f(x)"),
        dcc.Input(
            id="nonlin-f",
            type="text",
            placeholder="ej: x**2 - 5",
            className="input",
        ),

        html.Label("Valor inicial x0"),
        dcc.Input(
            id="nonlin-x0",
            type="number",
            placeholder="ej: 2.0",
            className="input",
        ),
    ]


def register_nonlinear_callbacks(app):

    # ============================================================
    # Callback 1: Construye el formulario dinámico
    # ============================================================
    @app.callback(
        Output("nonlin-input-area", "children"),
        Output("nonlin-g-card", "hidden"),
        Output("nonlin-x1-card", "hidden"),
        Output("nonlin-interval-card", "hidden"),
        Output("nonlin-btn-card", "hidden"),
        Input("nonlin-method", "value"),
        Input("nonlin-input-mode", "value"),
        prevent_initial_call=True,
    )
    def build_input_area(method, mode):

        if not method:
            return [], True, True, True, True

        # Área base: f(x) y x0
        area = _build_base_area()

        # Mostrar inputs según el método
        g_hidden = method != "fixed_point"
        x1_hidden = method != "secant"
        interval_hidden = method not in ["bisection", "false_position"]

        # Botón visible
        btn_hidden = False

        return area, g_hidden, x1_hidden, interval_hidden, btn_hidden

    # ============================================================
    # Callback 2: Ejecuta el cálculo
    # ============================================================
    @app.callback(
        Output("nonlin-result-area", "children"),
        Input("nonlin-run-btn", "n_clicks"),
        State("nonlin-method", "value"),
        State("nonlin-f", "value"),
        State("nonlin-x0", "value"),
        State("nonlin-x1", "value"),
        State("nonlin-g", "value"),
        State("nonlin-a", "value"),
        State("nonlin-b", "value"),
        prevent_initial_call=True,
    )
    def run_nonlinear(n_clicks, method, fn_expr, x0, x1, g_expr, a, b):

        if not method or not fn_expr:
            return no_update

        # Construcción de input_data
        input_data = {
            "mode": "function",
            "function": fn_expr,
            "calculation_mode": method,
            "tol": 1e-6,
            "max_iter": 50,
        }

        # Método: Newton / Fixed Point → requiere x0
        if method in ["newton", "fixed_point"]:
            input_data["x0"] = float(x0) if x0 is not None else None

        # Método: Secante → requiere x0 y x1
        if method == "secant":
            input_data["x0"] = float(x0) if x0 is not None else None
            input_data["x1"] = float(x1) if x1 is not None else None

        # Método: Bisección / Falsa Posición → requiere intervalo
        if method in ["bisection", "false_position"]:
            input_data["interval"] = [float(a), float(b)] if a is not None and b is not None else None

        # Método: Punto Fijo → requiere g(x)
        if method == "fixed_point":
            input_data["g"] = g_expr

        # Validación
        try:
            nm = NumericalMethod("nonlinear", input_data)
            nm.validate_input()
        except Exception as e:
            return contract.resolve(method, {
                "status":     "error",
                "error_type": "ValidationError",
                "message":    str(e),
                "context":    input_data,
            })

        # Ejecución
        try:
            outcome = nm.execute()
        except Exception as e:
            return contract.resolve(method, {
                "status":     "error",
                "error_type": "ExecutionError",
                "message":    str(e),
                "context":    input_data,
            })

        # Render final
        return contract.resolve(method, outcome)
