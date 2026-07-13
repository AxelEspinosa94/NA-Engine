# app/callbacks/linear_algebra_callbacks.py

import base64
import io
import re
import numpy as np
import pandas as pd

from dash import html, dcc, no_update
from dash.dependencies import Input, Output, State

from core.base_method import NumericalMethod
from core.contract import UIContract

contract = UIContract()


# ═══════════════════════════════════════════════════════════════
# REGISTER CALLBACKS
# ═══════════════════════════════════════════════════════════════

def register_linear_algebra_callbacks(app):

    # ============================================================
    # TOGGLE INPUT MODE (upload ↔ table)
    # ============================================================
    @app.callback(
        Output("la-upload-area", "hidden"),
        Output("la-table-area", "hidden"),
        Input("la-input-mode", "value"),
    )
    def toggle_input_mode(mode):
        if mode == "upload":
            return False, True
        return True, False

    # ============================================================
    # FILTER CALCULATION MODES BASED ON CALCULATION TYPE
    # ============================================================    
    @app.callback(
        Output("la-calculation-mode", "options"),
        Output("la-calculation-mode", "value"),
        Input("la-calculation-type", "value"),
        State("la-calculation-mode", "value"),
    )
    def filter_calculation_modes(calc_type, current_value):

        MATRIX_MODES = [
            {"label": "Determinant",        "value": "determinant"},
            {"label": "Inverse",            "value": "inverse"},
            {"label": "Norm",               "value": "norm"},
            {"label": "Condition Number",   "value": "condition_number"},
            {"label": "Transpose",          "value": "transpose"},
            {"label": "Rank",               "value": "rank"},
        ]

        SYSTEM_MODES = [
            {"label": "Gauss",              "value": "gauss"},
            {"label": "Gauss-Jordan",       "value": "gauss_jordan"},
            {"label": "LU",                 "value": "lu"},
            {"label": "Cholesky",           "value": "cholesky"},
            {"label": "QR",                 "value": "qr"},
            {"label": "Jacobi",             "value": "jacobi"},
            {"label": "Gauss-Seidel",       "value": "gauss_seidel"},
        ]

        # Select correct list
        if calc_type == "matrix_operations":
            options = MATRIX_MODES
        else:
            options = SYSTEM_MODES

        # If current value is not valid anymore, reset it
        valid_values = [opt["value"] for opt in options]
        if current_value not in valid_values:
            return options, None

        return options, current_value


    # ============================================================
    # RUN LINEAR ALGEBRA
    # ============================================================
    @app.callback(
        Output("linear-algebra-result-area", "children"),
        Input("la-run-btn", "n_clicks"),
        State("la-calculation-type", "value"),
        State("la-calculation-mode", "value"),
        State("la-input-mode", "value"),
        State("la-table-A", "data"),
        State("la-vector-b", "value"),
        State("la-upload", "contents"),
        State("la-upload", "filename"),
    )
    def run_linear_algebra(n_clicks, calc_type, mode, input_mode,
                           table_A, vector_b, upload_contents, upload_filename):

        if not n_clicks:
            return no_update

        # ───────────────────────────────────────────────
        # Build A and b depending on mode
        # ───────────────────────────────────────────────
        A, b = None, None

        # TABLE MODE
        if input_mode == "table":
            if table_A:
                try:
                    A = [[float(row[col]) for col in row] for row in table_A]
                except Exception:
                    return html.Div("Invalid numeric values in matrix A.", className="error")

            if calc_type == "ec-system":
                if not vector_b:
                    return html.Div("Vector b is required.", className="error")

                try:
                    b = [float(x) for x in re.split(r"[,\s|]+", vector_b.strip())]
                except Exception:
                    return html.Div("Invalid numeric values in vector b.", className="error")

        # UPLOAD MODE
        elif input_mode == "upload":
            A, b = _build_dataframe_from_upload(upload_contents, upload_filename)
            if A is None:
                return html.Div("Could not parse uploaded file.", className="error")

        # ───────────────────────────────────────────────
        # Build input_data
        # ───────────────────────────────────────────────
        input_data = {
            "A": A,
            "calculation_mode": mode,
            "calculation_type": calc_type,
        }

        if calc_type == "ec-system":
            input_data["b"] = b

        # ───────────────────────────────────────────────
        # Run NA‑Engine
        # ───────────────────────────────────────────────
        nm = NumericalMethod("linear_algebra", input_data)

        try:
            nm.validate_input()
            outcome = nm.execute()
        except Exception as e:
            return html.Div(str(e), className="error")

        payload = contract.resolve(mode, outcome)
        return payload


# ═══════════════════════════════════════════════════════════════
# UPLOAD PARSER
# ═══════════════════════════════════════════════════════════════

def _build_dataframe_from_upload(contents, filename):
    """
    Returns:
        - matrix A (list of lists)
        - vector b (optional)
    """

    if contents is None:
        return None, None

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    # ───────────────────────────────────────────────
    # TXT → matrix or system of equations
    # ───────────────────────────────────────────────
    if filename.endswith(".txt"):
        text = decoded.decode("utf-8")

        # Detect system of equations
        if "=" in text:
            A, b = _parse_linear_system_txt(text)
            return A, b

        # Otherwise assume matrix
        rows = text.strip().split("\n")
        try:
            A = [list(map(float, re.split(r"[,\s]+", row.strip()))) for row in rows]
        except Exception:
            return None, None

        return A, None

    # ───────────────────────────────────────────────
    # CSV
    # ───────────────────────────────────────────────
    if filename.endswith(".csv"):
        try:
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), header=None)
            return df.values.tolist(), None
        except Exception:
            return None, None

    # ───────────────────────────────────────────────
    # XLSX
    # ───────────────────────────────────────────────
    if filename.endswith(".xlsx"):
        try:
            df = pd.read_excel(io.BytesIO(decoded), header=None)
            return df.values.tolist(), None
        except Exception:
            return None, None

    return None, None


# ═══════════════════════════════════════════════════════════════
# LINEAR SYSTEM PARSER (TXT)
# ═══════════════════════════════════════════════════════════════

def _parse_linear_system_txt(text: str):
    """
    Parse a system of linear equations from a TXT file.

    Example:
        3x + 2y - z = 4
        x - y + 5z = 2

    Returns:
        A (matrix)
        b (vector)
    """

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    variables = []
    A = []
    b = []

    # First pass: detect variables
    for line in lines:
        vars_in_line = re.findall(r"[a-zA-Z]+", line.split("=")[0])
        for v in vars_in_line:
            if v not in variables:
                variables.append(v)

    variables.sort()  # enforce consistent ordering

    # Second pass: extract coefficients
    for line in lines:
        left, right = line.split("=")
        right = float(right.strip())

        coeffs = []
        for var in variables:
            pattern = rf"([+-]?\s*\d*\.?\d*)\s*{var}"
            match = re.search(pattern, left.replace(" ", ""))
            if match:
                raw = match.group(1)
                if raw in ["", "+", "-"]:
                    raw += "1"
                coeffs.append(float(raw))
            else:
                coeffs.append(0.0)

        A.append(coeffs)
        b.append(right)

    return A, b
