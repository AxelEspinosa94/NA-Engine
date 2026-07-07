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

# n razonables por método para STRESS (no accuracy)
N_STRESS = {
    "trapezoid_simple":    1,     # por definición
    "trapezoid_composite": 300,   # suficientemente grande
    "simpson_1_3":         300,   # suficientemente grande
    "simpson_3_8":         300,   # múltiplo de 3
    "romberg":             6,     # romberg explota con n grande
    "gauss":               15,    # gauss estable y rápido
}

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


# ────────────────────────────────────────────────────────────────
# STRESS: volumen de subintervalos (solo estabilidad)
# ────────────────────────────────────────────────────────────────

@pytest.mark.pending
@pytest.mark.parametrize("method", METHODS)
def test_volumen_stress(method):
    """El método debe soportar n grande sin explotar."""
    n = N_STRESS[method]
    outcome = make_outcome(method, "x**2", [0, 1], n)
    assert outcome["status"] == "success"
    assert "value" in outcome["result"]


# ────────────────────────────────────────────────────────────────
# STRESS: determinismo
# ────────────────────────────────────────────────────────────────

@pytest.mark.pending
@pytest.mark.parametrize("method", METHODS)
def test_determinismo(method):
    """El mismo input debe producir el mismo output."""
    n = N_STRESS[method]
    outcome_1 = make_outcome(method, "x**2", [0, 1], n)
    outcome_2 = make_outcome(method, "x**2", [0, 1], n)
    assert outcome_1["result"]["value"] == outcome_2["result"]["value"]


# ────────────────────────────────────────────────────────────────
# STRESS: intervalos negativos
# ────────────────────────────────────────────────────────────────

@pytest.mark.pending
@pytest.mark.parametrize("method", METHODS)
def test_intervalo_negativo(method):
    """Intervalos negativos deben funcionar sin explotar."""
    n = N_STRESS[method]
    outcome = make_outcome(method, "x**2", [-1, 1], n)
    assert outcome["status"] == "success"


# ────────────────────────────────────────────────────────────────
# STRESS: intervalos unitarios
# ────────────────────────────────────────────────────────────────

@pytest.mark.pending
@pytest.mark.parametrize("method", METHODS)
def test_intervalo_unitario(method):
    """Intervalo de longitud 1 debe funcionar sin explotar."""
    n = N_STRESS[method]
    outcome = make_outcome(method, "x**3", [0, 1], n)
    assert outcome["status"] == "success"


# ────────────────────────────────────────────────────────────────
# STRESS: funciones sin primitiva elemental
# ────────────────────────────────────────────────────────────────

@pytest.mark.pending
@pytest.mark.parametrize("method", [
    "trapezoid_composite",
    "simpson_1_3",
    "simpson_3_8",
    "romberg",
    "gauss",
])
def test_funcion_sin_primitiva_gaussiana(method):
    """e^(-x²) debe producir un resultado o error controlado."""
    n = N_STRESS[method]
    outcome = make_outcome(method, "exp(-x**2)", [0, 1], n)
    assert outcome["status"] in ("success", "error")


@pytest.mark.pending
@pytest.mark.parametrize("method", [
    "trapezoid_composite",
    "simpson_1_3",
    "simpson_3_8",
    "romberg",
    "gauss",
])
def test_funcion_sin_primitiva_sinc(method):
    """sin(x)/x debe producir resultado o error controlado."""
    n = N_STRESS[method]
    outcome = make_outcome(method, "sin(x)/x", [0.001, np.pi], n)
    assert outcome["status"] in ("success", "error")


@pytest.mark.pending
@pytest.mark.parametrize("method", [
    "trapezoid_composite",
    "simpson_1_3",
])
def test_funcion_con_singularidad(method):
    """1/x debe producir error controlado, no crash."""
    n = N_STRESS[method]
    outcome = make_outcome(method, "1/x", [0, 1], n)
    assert outcome["status"] in ("success", "error")


# ────────────────────────────────────────────────────────────────
# STRESS: estructura del resultado
# ────────────────────────────────────────────────────────────────

@pytest.mark.pending
@pytest.mark.parametrize("method", METHODS)
def test_estructura_resultado(method):
    """El resultado debe contener las claves esperadas."""
    n = N_STRESS[method]
    outcome = make_outcome(method, "x**2", [0, 1], n)
    assert outcome["status"] == "success"
    result = outcome["result"]
    required_keys = ["value", "x", "y", "a", "b", "n", "calculation_mode"]
    for key in required_keys:
        assert key in result


# ────────────────────────────────────────────────────────────────
# STRESS: UIContract
# ────────────────────────────────────────────────────────────────

@pytest.mark.pending
@pytest.mark.parametrize("method", METHODS)
def test_contract_devuelve_div(method):
    """UIContract debe devolver un html.Div válido."""
    n = N_STRESS[method]
    outcome = make_outcome(method, "x**2", [0, 1], n)
    result = contract.resolve(method, outcome)
    assert isinstance(result, html.Div)
    assert result.children


@pytest.mark.pending
@pytest.mark.parametrize("method", METHODS)
def test_contract_error_devuelve_div(method):
    """UIContract debe manejar errores sin explotar."""
    outcome = {
        "status":     "error",
        "error_type": "ValidationError",
        "message":    "Test error",
        "context":    {},
    }
    result = contract.resolve(method, outcome)
    assert isinstance(result, html.Div)
