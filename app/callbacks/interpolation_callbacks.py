# app/callbacks/interpolation_callbacks.py
import pandas as pd
import numpy as np
import sympy as sp
import base64
import io
from dash import Input, Output, State, callback, html, dcc, dash_table
from dash import no_update
from core.base_method import NumericalMethod
from core.contract import UIContract
from core.exceptions import ValidationError, InputError

def _build_dataframe_from_function(method: str, fn_expr: str, a: float, b: float, n: int) -> pd.DataFrame:
    """
    Construye un DataFrame evaluando una función f(x) en n puntos entre [a, b].
    Si el método es hermite, también calcula f'(x).
    """

    # Validaciones básicas
    if not fn_expr:
        raise InputError("Debes ingresar una función f(x).")

    if n <= 1:
        raise InputError("El número de puntos debe ser mayor a 1.")

    # Construir vector de puntos
    xs = np.linspace(float(a), float(b), int(n))

    # Preparar entorno seguro para eval
    def safe_eval(expr, x):
        try:
            return float(eval(expr, {"__builtins__": {}}, {"x": x, "np": np}))
        except Exception as e:
            raise ValidationError(f"Error evaluando f(x): {e}")

    # Evaluar f(x)
    ys = [safe_eval(fn_expr, x) for x in xs]

    # Si es Hermite, calcular derivada simbólica
    if method == "hermite":
        x_sym = sp.symbols("x")
        try:
            f_sym = sp.sympify(fn_expr)
            df_sym = sp.diff(f_sym, x_sym)
            dys = [float(df_sym.subs(x_sym, x)) for x in xs]
        except Exception as e:
            raise ValidationError(f"Error calculando derivada: {e}")

        return pd.DataFrame({"x": xs, "y": ys, "dy": dys})

    # Métodos normales
    return pd.DataFrame({"x": xs, "y": ys})

def _build_dataframe_from_upload(method: str, contents: str, filename: str) -> pd.DataFrame:
    """
    Construye un DataFrame a partir de un archivo cargado vía dcc.Upload.
    Soporta CSV, TXT, Excel, JSON.
    """

    if contents is None:
        raise ValidationError("No se ha cargado ningún archivo.")

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    # Detectar tipo de archivo
    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

        elif filename.endswith(".txt"):
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), sep=None, engine="python")

        elif filename.endswith(".xlsx") or filename.endswith(".xls"):
            df = pd.read_excel(io.BytesIO(decoded))

        elif filename.endswith(".json"):
            df = pd.read_json(io.StringIO(decoded.decode("utf-8")))

        else:
            raise ValidationError(f"Formato no soportado: {filename}")

    except Exception as e:
        raise ValidationError(f"Error leyendo archivo: {e}")

    # Validar columnas según método
    required = ["x", "y", "dy"] if method == "hermite" else ["x", "y"]

    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValidationError(f"Faltan columnas requeridas: {missing}")

    # Convertir a numérico y limpiar
    df = df[required].apply(pd.to_numeric, errors="coerce").dropna()

    return df

def _build_dataframe(method: str, mode: str, table_data=None, fn_expr=None, a=None, b=None, n=None, upload_contents=None, upload_filename=None):
    if mode == "table":
        columns = ["x", "y", "dy"] if method == "hermite" else ["x", "y"]
        df = pd.DataFrame(table_data)
        df = df[columns].apply(pd.to_numeric, errors="coerce").dropna()
        return df

    if mode == "function":
        return _build_dataframe_from_function(method, fn_expr, a, b, n)

    if mode == "upload":
        return _build_dataframe_from_upload(method, upload_contents, upload_filename)

    raise NotImplementedError(f"Modo '{mode}' no implementado.")


def _build_mode_area(method: str, mode: str) -> list:
    # columnas según método
    columns = ["x", "y", "dy"] if method == "hermite" else ["x", "y"]
    if mode == "function":
        return [
            html.Label("Función f(x)"),
            dcc.Input(id="interp-fn",  type="text",
                    placeholder="ej: x**2 + 1", className="input"),
            html.Label("Rango"),
            html.Div(className="input-row", children=[
                dcc.Input(id="interp-a", type="number",
                        placeholder="a", className="input"),
                dcc.Input(id="interp-b", type="number",
                        placeholder="b", className="input"),
            ]),
            html.Label("Número de puntos"),
            dcc.Input(id="interp-n", type="number",
                    placeholder="ej: 10", className="input"),
        ]
    if mode == "upload":
        return [
            dcc.Upload(
                id="interp-upload",
                children=html.Div(["Arrastra o ", html.A("selecciona un archivo")]),
                className="upload-area",
                accept=".csv,.txt",
            ),
            html.Div(id="interp-upload-preview"),
        ]
    # mode == "table" (default)
    return [
        dash_table.DataTable(
            id="interp-table",
            columns=[{"name": c, "id": c, "editable": True} for c in columns],
            data=[{c: "" for c in columns} for _ in range(5)],
            editable=True,
            row_deletable=True,
            #row_addable=True,  # si tu versión de Dash lo soporta
        ),
    ]

contract = UIContract()

def register_interpolation_callbacks(app):

    # ── Callback 1: construye el formulario ─────────────────────────────────────
    @app.callback(
        Output("interp-input-area",  "children"),
        Output("interp-mode-card",   "hidden"),
        Output("interp-xk-card",     "hidden"),
        Output("interp-btn-card",    "hidden"),
        Input("interp-method",       "value"),
        Input("interp-input-mode",   "value"),
        prevent_initial_call=True,
    )
    def build_input_area(method, mode):
        if not method:
            return [], True, True, True
        if mode == "upload":
            area = _build_mode_area(method, mode)
            return area, False, False, False
        return no_update, no_update, no_update, no_update

    # ── Callback 2: ejecuta el cálculo ──────────────────────────────────────────
    @app.callback(
        Output("interp-result-area", "children"),
        Input("interp-run-btn",      "n_clicks"),
        State("interp-method",       "value"),
        State("interp-input-mode",   "value"),
        State("interp-xk",           "value"),
        # table mode
        State("interp-table",        "data"),
        State("interp-fn", "value"),
        State("interp-a", "value"),
        State("interp-b", "value"),
        State("interp-n", "value"),
        State("interp-upload", "contents"),
        State("interp-upload", "filename"),
        prevent_initial_call=True,
    )
    def run_interpolation(n_clicks, method, mode, xk, 
                    table_data=None, fn_expr=None, a=None, b=None, n=None, upload_contents=None, upload_filename=None):
        if not method or xk is None:
            #return html.P("Completa todos los campos.", className="result-warning")
            return no_update

        try:
            df = _build_dataframe(
                method, mode,
                table_data=table_data,
                fn_expr=fn_expr,
                a=a, b=b, n=n,
                upload_contents=upload_contents,
                upload_filename=upload_filename
            )
        except Exception as e:
            return contract.resolve(method, {
                "status":     "error",
                "error_type": "InputError",
                "message":    f"Error al construir el DataFrame: {e}",
                "context":    {},
            })

        input_data = {
            "mode":             "table",
            "data":             df,
            "xk":               float(xk),
            "calculation_mode": method,
        }

        try:
            nm = NumericalMethod("interpolation", input_data)
            nm.validate_input()
        except ValidationError as e:
            return contract.resolve(method, {
                "status":     "error",
                "error_type": "ValidationError",
                "message":    str(e),
                "context":    input_data,
            })

        outcome = nm.execute()
        return contract.resolve(method, outcome)
    
    # ── Callback 3: agrega filas a la tabla ──────────────────────────────────────────
    @app.callback(
        Output("interp-table", "data"),
        Input("interp-add-row-btn", "n_clicks"),
        State("interp-table", "data"),
        State("interp-table", "columns"),
        prevent_initial_call=True,
    )
    def add_row(n_clicks, rows, columns):
        if not n_clicks:
            return no_update
        rows.append({c["id"]: "" for c in columns})
        return rows