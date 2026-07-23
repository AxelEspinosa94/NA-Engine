# app/callbacks/derivative_callbacks.py

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

def _build_input_area():
    """
    Área dinámica para derivadas numéricas.
    Siempre incluye:
    - función f(x)
    - x
    - h
    """
    return [
        html.Label("Función f(x)"),
        dcc.Input(
            id="deriv-function",
            type="text",
            placeholder="ej: x**2 + 3*x",
            className="input",
        ),

        html.Label("Valor de x"),
        dcc.Input(
            id="deriv-x",
            type="number",
            placeholder="ej: 2.0",
            className="input",
        ),

        html.Label("Paso h"),
        dcc.Input(
            id="deriv-h",
            type="number",
            placeholder="ej: 0.01",
            className="input",
        ),
    ]


def register_derivative_callbacks(app):

    # ============================================================
    # Callback 1: Construye el formulario dinámico
    # ============================================================
    @app.callback(
        Output("deriv-input-area", "children"),
        Output("deriv-y-card", "hidden"),
        Output("deriv-btn-card", "hidden"),
        Input("deriv-method", "value"),
        Input("deriv-input-mode", "value"),
        prevent_initial_call=True,
    )
    def build_input_area(method, mode):

        if not method:
            return [], True, True

        # Área dinámica (siempre función + x + h)
        area = _build_input_area()

        # Mostrar y solo para parciales
        y_hidden = method not in ["partial_x", "partial_y"]

        # Botón visible
        btn_hidden = False

        return area, y_hidden, btn_hidden

    # ============================================================
    # Callback 2: Ejecuta el cálculo
    # ============================================================
    @app.callback(
        Output("deriv-result-area", "children"),
        Input("deriv-run-btn", "n_clicks"),
        State("deriv-method", "value"),
        State("deriv-function", "value"),
        State("deriv-x", "value"),
        State("deriv-h", "value"),
        State("deriv-y", "value"),
        prevent_initial_call=True,
    )
    def run_derivative(n_clicks, method, fn_expr, x, h, y):

        # Validación básica de UI
        if not method or not fn_expr or x is None or h is None:
            return no_update

        # Construir input_data para NumericalMethod
        input_data = {
            "function": fn_expr,
            "x": float(x),
            "h": float(h),
            "calculation_mode": method,
        }

        # Parciales requieren y
        if method in ["partial_x", "partial_y"]:
            input_data["y"] = float(y)

        # Richardson requiere orden
        if method == "richardson":
            input_data["richardson_order"] = 2

        # Validación
        try:
            nm = NumericalMethod("numerical_derivative", input_data)
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
