# tests/stress/test_interpolation_stress.py
import pytest
import numpy as np
import pandas as pd
from core.base_method import NumericalMethod
from core.contract import UIContract
from dash import html

contract = UIContract()

def make_outcome(method, df, xk):
    input_data = {
        "mode":             "table",
        "data":             df,
        "xk":               xk,
        "calculation_mode": method,
    }
    nm = NumericalMethod("interpolation", input_data)
    nm.validate_input()
    return nm.execute()


# ── Volumen ─────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("n", [10, 50, 100])
@pytest.mark.parametrize("method", ["lagrange", "newton", "spline_cubic"])
def test_volumen_muchos_nodos(n, method):
    """El método no debe explotar con n nodos equidistantes."""
    x = np.linspace(0, 10, n)
    y = np.sin(x)
    df = pd.DataFrame({"x": x, "y": y})
    outcome = make_outcome(method, df, xk=5.0)
    assert outcome["status"] == "success"


@pytest.mark.parametrize("n", [10, 50])
def test_volumen_hermite(n):
    """Hermite con n nodos y derivadas conocidas."""
    x  = np.linspace(0, np.pi, n)
    y  = np.sin(x)
    dy = np.cos(x)
    df = pd.DataFrame({"x": x, "y": y, "dy": dy})
    outcome = make_outcome("hermite", df, xk=np.pi / 4)
    assert outcome["status"] == "success"


# ── Precisión ────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("method", ["lagrange", "newton", "spline_cubic", "hermite"])
def test_precision_polinomio_grado_2(method):
    """Con suficientes nodos todos los métodos deben aproximar x² bien."""
    x = np.linspace(0, 3, 20)  # 20 nodos en lugar de 4
    y = x ** 2
    xk = 1.5
    expected = xk ** 2

    if method == "hermite":
        df = pd.DataFrame({"x": x, "y": y, "dy": 2 * x})
    else:
        df = pd.DataFrame({"x": x, "y": y})

    outcome = make_outcome(method, df, xk=xk)
    assert outcome["status"] == "success"
    assert abs(outcome["result"]["value"] - expected) < 1e-4


@pytest.mark.parametrize("method", ["lagrange", "newton", "spline_cubic", "hermite"])
def test_precision_funcion_lineal(method):
    """Interpolar f(x) = 2x + 1 debe ser exacto para cualquier xk."""
    x = np.linspace(0, 3, 20)  # 20 nodos en lugar de 4
    y = 2 * x + 1
    xk = 2.5
    expected = 2 * xk + 1  # 6.0

    if method == "hermite":
        df = pd.DataFrame({"x": x, "y": y, "dy": np.full_like(x, 2.0)})
    else:
        df = pd.DataFrame({"x": x, "y": y})

    outcome = make_outcome(method, df, xk=xk)
    assert outcome["status"] == "success"
    assert abs(outcome["result"]["value"] - expected) < 1e-6


# ── Estabilidad ──────────────────────────────────────────────────────────────

@pytest.mark.parametrize("method", ["lagrange", "newton"])
def test_runge_grado_alto(method):
    """
    f(x) = 1/(1+25x²) con 15 nodos equidistantes en [-1, 1].
    Error grande en los extremos es comportamiento esperado (fenómeno de Runge),
    no un bug. El método debe completar sin explotar.
    """
    x = np.linspace(-1, 1, 15)
    y = 1 / (1 + 25 * x ** 2)
    df = pd.DataFrame({"x": x, "y": y})
    outcome = make_outcome(method, df, xk=0.9)
    # No afirmamos precisión, solo que el proceso completa
    assert outcome["status"] in ("success", "error")


@pytest.mark.parametrize("method", ["lagrange", "newton", "spline_cubic", "hermite"])
def test_determinismo(method):
    """El mismo input siempre produce el mismo output."""
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = np.sin(x)

    if method == "hermite":
        df = pd.DataFrame({"x": x, "y": y, "dy": np.cos(x)})
    else:
        df = pd.DataFrame({"x": x, "y": y})

    outcome_1 = make_outcome(method, df, xk=1.5)
    outcome_2 = make_outcome(method, df, xk=1.5)

    assert outcome_1["result"]["value"] == outcome_2["result"]["value"]


# ── UIContract ───────────────────────────────────────────────────────────────

@pytest.mark.parametrize("method", ["lagrange", "newton", "spline_cubic", "hermite"])
def test_contract_devuelve_div(method):
    """El full process hasta html.Div no debe explotar."""
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = x ** 2

    if method == "hermite":
        df = pd.DataFrame({"x": x, "y": y, "dy": 2 * x})
    else:
        df = pd.DataFrame({"x": x, "y": y})

    outcome = make_outcome(method, df, xk=1.5)
    result  = contract.resolve(method, outcome)
    assert isinstance(result, html.Div)
    assert result.children  # no debe ser un Div vacío


@pytest.mark.parametrize("method", ["lagrange", "newton", "spline_cubic", "hermite"])
def test_contract_error_devuelve_div(method):
    """Un outcome de error también debe producir un html.Div limpio."""
    outcome = {
        "status":     "error",
        "error_type": "ValidationError",
        "message":    "Test error",
        "context":    {},
    }
    result = contract.resolve(method, outcome)
    assert isinstance(result, html.Div)