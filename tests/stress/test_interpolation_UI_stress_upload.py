# tests/stress/test_interpolation_upload.py
import pytest
import base64
import io
import numpy as np
import pandas as pd
from core.base_method import NumericalMethod
from core.contract import UIContract
from core.exceptions import ValidationError
from app.callbacks.interpolation_callbacks import _build_dataframe_from_upload
from dash import html

contract = UIContract()

# ── Helpers ─────────────────────────────────────────────────────────────────

def make_df(n: int, method: str) -> pd.DataFrame:
    x = np.linspace(0, 10, n)
    y = np.sin(x)
    if method == "hermite":
        return pd.DataFrame({"x": x, "y": y, "dy": np.cos(x)})
    return pd.DataFrame({"x": x, "y": y})


def encode_csv(df: pd.DataFrame) -> str:
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    encoded = base64.b64encode(buffer.getvalue().encode()).decode()
    return f"data:text/csv;base64,{encoded}"


def encode_txt(df: pd.DataFrame, sep="\t") -> str:
    buffer = io.StringIO()
    df.to_csv(buffer, index=False, sep=sep)
    encoded = base64.b64encode(buffer.getvalue().encode()).decode()
    return f"data:text/plain;base64,{encoded}"


def encode_excel(df: pd.DataFrame) -> str:
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    encoded = base64.b64encode(buffer.getvalue()).decode()
    return f"data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{encoded}"


def encode_json(df: pd.DataFrame) -> str:
    encoded = base64.b64encode(df.to_json().encode()).decode()
    return f"data:application/json;base64,{encoded}"


# ── Formatos ─────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("method", ["lagrange", "newton", "spline_cubic"])
def test_upload_csv(method):
    df = make_df(20, method)
    result = _build_dataframe_from_upload(method, encode_csv(df), "data.csv")
    assert list(result.columns) == ["x", "y"]
    assert len(result) == 20


@pytest.mark.parametrize("method", ["lagrange", "newton", "spline_cubic"])
def test_upload_txt(method):
    df = make_df(20, method)
    result = _build_dataframe_from_upload(method, encode_txt(df), "data.txt")
    assert list(result.columns) == ["x", "y"]
    assert len(result) == 20


@pytest.mark.parametrize("method", ["lagrange", "newton", "spline_cubic"])
def test_upload_excel(method):
    df = make_df(20, method)
    result = _build_dataframe_from_upload(method, encode_excel(df), "data.xlsx")
    assert list(result.columns) == ["x", "y"]
    assert len(result) == 20


@pytest.mark.parametrize("method", ["lagrange", "newton", "spline_cubic"])
def test_upload_json(method):
    df = make_df(20, method)
    result = _build_dataframe_from_upload(method, encode_json(df), "data.json")
    assert list(result.columns) == ["x", "y"]
    assert len(result) == 20


def test_upload_hermite_csv():
    """Hermite requiere columna dy."""
    df = make_df(20, "hermite")
    result = _build_dataframe_from_upload("hermite", encode_csv(df), "data.csv")
    assert list(result.columns) == ["x", "y", "dy"]
    assert len(result) == 20


# ── Volumen ──────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("n", [50, 200, 500])
def test_upload_volumen_csv(n):
    """CSV con n filas debe parsearse completo."""
    df = make_df(n, "lagrange")
    result = _build_dataframe_from_upload("lagrange", encode_csv(df), "data.csv")
    assert len(result) == n


# ── Errores controlados ───────────────────────────────────────────────────────

def test_upload_none_contents():
    """Sin archivo debe lanzar ValidationError."""
    with pytest.raises(ValidationError):
        _build_dataframe_from_upload("lagrange", None, "data.csv")


def test_upload_formato_no_soportado():
    """Formato desconocido debe lanzar ValidationError."""
    df = make_df(10, "lagrange")
    contents = encode_csv(df).replace("text/csv", "text/xml")
    with pytest.raises(ValidationError):
        _build_dataframe_from_upload("lagrange", contents, "data.xml")


def test_upload_columnas_faltantes():
    """CSV sin columna y debe lanzar ValidationError."""
    df = pd.DataFrame({"x": np.linspace(0, 10, 10)})
    with pytest.raises(ValidationError):
        _build_dataframe_from_upload("lagrange", encode_csv(df), "data.csv")


def test_upload_hermite_sin_dy():
    """CSV sin columna dy para Hermite debe lanzar ValidationError."""
    df = pd.DataFrame({"x": np.linspace(0, 10, 10), "y": np.sin(np.linspace(0, 10, 10))})
    with pytest.raises(ValidationError):
        _build_dataframe_from_upload("hermite", encode_csv(df), "data.csv")


def test_upload_columnas_extra_ignoradas():
    """Columnas extra en el CSV deben ignorarse."""
    x = np.linspace(0, 10, 20)
    df = pd.DataFrame({"x": x, "y": np.sin(x), "z": x**2, "w": x**3})
    result = _build_dataframe_from_upload("lagrange", encode_csv(df), "data.csv")
    assert list(result.columns) == ["x", "y"]


# ── Full process ──────────────────────────────────────────────────────────────

@pytest.mark.parametrize("method", ["lagrange", "newton", "spline_cubic"])
@pytest.mark.parametrize("n", [20, 100])
def test_full_process_upload(method, n):
    """Upload → DataFrame → NumericalMethod → UIContract → html.Div."""
    df_original = make_df(n, method)
    df = _build_dataframe_from_upload(method, encode_csv(df_original), "data.csv")

    input_data = {
        "mode":             "upload",
        "data":             df,
        "xk":               5.0,
        "calculation_mode": method,
    }
    nm = NumericalMethod("interpolation", input_data)
    nm.validate_input()
    outcome = nm.execute()
    result = contract.resolve(method, outcome)

    assert outcome["status"] == "success"
    assert isinstance(result, html.Div)
    assert result.children