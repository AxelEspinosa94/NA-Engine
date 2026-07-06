# tests/stress/test_integration_stress.py
import pytest
import numpy as np
from core.base_method import NumericalMethod
from core.contract import UIContract
from dash import html

contract = UIContract()

METHODS = [
    "trapezoid_simple",
    "trapezoid_composite",
    "simpson_1_3",
    "simpson_3_8",
    "romberg",
    "gauss",
]

# n razonables por método — romberg y gauss son muy sensibles a n grande
MIN_N = {
    "trapezoid_simple":    1,
    "trapezoid_composite": 2,
    "simpson_1_3":         2,
    "simpson_3_8":         3,
    "romberg":             2,
    "gauss":               2,
}

MAX_N = {
    "trapezoid_simple":    1,   # por definición es n=1
    "trapezoid_composite": 500,
    "simpson_1_3":         500,
    "simpson_3_8":         500,
    "romberg":             6,   # 2^6 = 64 evaluaciones, suficiente
    "gauss":               20,  # gauss con muchos puntos es exacto y rápido
}


# ── Helper ───────────────────────────────────────────────────────────────────

def make_outcome(method: str, function: str, interval: list, n: int):
    input_data = {
        "mode":             "function",
        "function":         function,
        "interval":         interval,
        "n":                n,
        "calculation_mode": method,
    }
    nm = NumericalMethod("integration", input_data)
    nm.validate_input()
    return nm.execute()


# ── Volumen: número de subintervalos ─────────────────────────────────────────

@pytest.mark.pending
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("n", [10, 50, 100, 500])
def test_volumen_subintervalos(method, n):
    """El método no debe explotar con n subintervalos."""
    n_actual = max(MIN_N[method], min(n, MAX_N[method]))
    outcome = make_outcome(method, "x**2", [0, 1], n_actual)
    assert outcome["status"] == "success"
    assert "value" in outcome["result"]


# ── Precisión: resultados con primitiva conocida ──────────────────────────────

@pytest.mark.pending
@pytest.mark.parametrize("method,tol", [
    ("trapezoid_simple",    1e-1),   # un solo tramo, error grande esperado
    ("trapezoid_composite", 1e-3),
    ("simpson_1_3",         1e-6),
    ("simpson_3_8",         1e-6),
    ("romberg",             1e-8),
    ("gauss",               1e-8),
])
def test_precision_polinomio_grado_2(method, tol):
    """Integral de x² en [0,1] = 1/3 exacto."""
    n = max(100, MIN_N[method])
    outcome = make_outcome(method, "x**2", [0, 1], n)
    assert outcome["status"] == "success"
    assert abs(outcome["result"]["value"] - 1/3) < tol


@pytest.mark.pending
@pytest.mark.parametrize("method,tol", [
    ("trapezoid_simple",    1e-1),
    ("trapezoid_composite", 1e-4),
    ("simpson_1_3",         1e-6),
    ("simpson_3_8",         1e-6),
    ("romberg",             1e-8),
    ("gauss",               1e-8),
])
def test_precision_funcion_trigonometrica(method, tol):
    """Integral de sin(x) en [0, pi] = 2 exacto."""
    import math
    n = max(100, MIN_N[method])
    outcome = make_outcome(method, "sin(x)", [0, math.pi], n)
    assert outcome["status"] == "success"
    assert abs(outcome["result"]["value"] - 2.0) < tol


@pytest.mark.pending
@pytest.mark.parametrize("method,tol", [
    ("trapezoid_composite", 1e-3),
    ("simpson_1_3",         1e-6),
    ("romberg",             1e-8),
    ("gauss",               1e-8),
])
def test_precision_funcion_exponencial(method, tol):
    """Integral de e^x en [0,1] = e - 1 exacto."""
    import math
    n = max(100, MIN_N[method])
    outcome = make_outcome(method, "exp(x)", [0, 1], n)
    assert outcome["status"] == "success"
    assert abs(outcome["result"]["value"] - (math.e - 1)) < tol


# ── Estabilidad ───────────────────────────────────────────────────────────────

@pytest.mark.pending
@pytest.mark.parametrize("method", METHODS)
def test_determinismo(method):
    """El mismo input siempre produce el mismo output."""
    n = max(10, MIN_N[method])
    outcome_1 = make_outcome(method, "x**2", [0, 1], n)
    outcome_2 = make_outcome(method, "x**2", [0, 1], n)
    assert outcome_1["result"]["value"] == outcome_2["result"]["value"]


@pytest.mark.pending
@pytest.mark.parametrize("method", [
    "trapezoid_composite",
    "simpson_1_3",
    "romberg",
    "gauss",
])
def test_intervalo_negativo(method):
    """Intervalo [a, b] con a < 0 debe funcionar correctamente."""
    n = max(10, MIN_N[method])
    outcome = make_outcome(method, "x**2", [-1, 1], n)
    assert outcome["status"] == "success"
    # integral de x² en [-1,1] = 2/3
    assert abs(outcome["result"]["value"] - 2/3) < 1e-3


@pytest.mark.pending
@pytest.mark.parametrize("method", METHODS)
def test_intervalo_unitario(method):
    """Intervalo de longitud 1 debe funcionar sin explotar."""
    n = max(10, MIN_N[method])
    outcome = make_outcome(method, "x**3", [0, 1], n)
    assert outcome["status"] == "success"


# ── Funciones sin primitiva elemental ────────────────────────────────────────

@pytest.mark.pending
@pytest.mark.parametrize("method", [
    "trapezoid_composite",
    "simpson_1_3",
    "romberg",
    "gauss",
])
def test_funcion_sin_primitiva_gaussiana(method):
    """
    e^(-x²) no tiene primitiva elemental (función de error).
    El método numérico debe completar y devolver un resultado aproximado.
    sympy puede devolver None o la integral sin evaluar — el sistema
    no debe explotar en ningún caso.
    Valor de referencia: integral de e^(-x²) en [0,1] ≈ 0.7468
    """
    n = max(50, MIN_N[method])
    outcome = make_outcome(method, "exp(-x**2)", [0, 1], n)
    # el proceso debe completar, sea success o error controlado
    assert outcome["status"] in ("success", "error")
    if outcome["status"] == "success":
        assert abs(outcome["result"]["value"] - 0.7468) < 1e-2


@pytest.mark.pending
@pytest.mark.parametrize("method", [
    "trapezoid_composite",
    "simpson_1_3",
    "romberg",
    "gauss",
])
def test_funcion_sin_primitiva_sinc(method):
    """
    sin(x)/x (sinc) no tiene primitiva elemental.
    Valor de referencia: integral de sin(x)/x en [0.001, pi] ≈ 1.5708
    (evitamos x=0 por la singularidad removible)
    """
    n = max(50, MIN_N[method])
    outcome = make_outcome(method, "sin(x)/x", [0.001, np.pi], n)
    assert outcome["status"] in ("success", "error")
    if outcome["status"] == "success":
        assert abs(outcome["result"]["value"] - 1.5708) < 1e-2


@pytest.mark.pending
@pytest.mark.parametrize("method", [
    "trapezoid_composite",
    "simpson_1_3",
])
def test_funcion_con_singularidad(method):
    """
    1/x tiene singularidad en x=0. Si el intervalo incluye o
    se acerca a 0, el sistema debe devolver error controlado, no explotar.
    """
    outcome = make_outcome(method, "1/x", [0, 1], 10)
    # esperamos error controlado, no excepción no manejada
    assert outcome["status"] in ("success", "error")


# ── Estructura del resultado ──────────────────────────────────────────────────

@pytest.mark.pending
@pytest.mark.parametrize("method", METHODS)
def test_estructura_resultado(method):
    """El resultado debe contener las claves esperadas."""
    n = max(10, MIN_N[method])
    outcome = make_outcome(method, "x**2", [0, 1], n)
    assert outcome["status"] == "success"
    result = outcome["result"]
    required_keys = ["value", "x", "y", "a", "b", "n", "calculation_mode"]
    for key in required_keys:
        assert key in result, f"Clave faltante: {key}"


# ── UIContract ────────────────────────────────────────────────────────────────

@pytest.mark.pending
@pytest.mark.parametrize("method", METHODS)
def test_contract_devuelve_div(method):
    """El full process hasta html.Div no debe explotar."""
    n = max(10, MIN_N[method])
    outcome = make_outcome(method, "x**2", [0, 1], n)
    result = contract.resolve(method, outcome)
    assert isinstance(result, html.Div)
    assert result.children


@pytest.mark.pending
@pytest.mark.parametrize("method", METHODS)
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