import numpy as np
import pytest

from core.base_method import NumericalMethod

METHODS = [
    "trapezoid_composite",
    "simpson_1_3",
    "simpson_3_8",
    "romberg",
    #    "gauss", # These tests are not suitable for Gauss due to its inhability to handle singularities and non-elementary functions.
    "clenshaw_curtis",
]

# n preferentes por método (válidos y razonables)
N_REG = {
    "trapezoid_composite": 200,
    "simpson_1_3": 200,
    "simpson_3_8": 198,  # múltiplo de 3
    "romberg": 6,
    "gauss": 12,
    "clenshaw_curtis": 40,
}

# tolerancias razonables por método
TOL_REG = {
    "trapezoid_composite": 1e-3,
    "simpson_1_3": 1e-6,
    "simpson_3_8": 1e-6,
    "romberg": 1e-8,
    "gauss": 1e-5,
    "clenshaw_curtis": 1e-10,
}


def make_outcome(method: str, function: str, interval: list):
    n = N_REG[method]
    nm = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": function,
            "interval": interval,
            "n": n,
            "calculation_mode": method,
        },
    )
    nm.validate_input()
    return nm.execute()


# ────────────────────────────────────────────────────────────────
# REGRESIÓN: funciones trigonométricas
# ────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("method", METHODS)
def test_regresion_sin(method):
    """∫₀^π sin(x) dx = 2"""
    tol = TOL_REG[method]
    outcome = make_outcome(method, "sin(x)", [0, np.pi])
    assert outcome["status"] == "success"
    assert abs(outcome["result"]["value"] - 2) < tol


@pytest.mark.parametrize("method", METHODS)
def test_regresion_cos(method):
    """∫₀^π cos(x) dx = 0"""
    tol = TOL_REG[method]
    outcome = make_outcome(method, "cos(x)", [0, np.pi])
    assert outcome["status"] == "success"
    assert abs(outcome["result"]["value"] - 0) < tol


@pytest.mark.parametrize("method", METHODS)
def test_regresion_sin2(method):
    """∫₀^π sin²(x) dx = π/2"""
    exact = np.pi / 2
    tol = TOL_REG[method]
    outcome = make_outcome(method, "sin(x)**2", [0, np.pi])
    assert outcome["status"] == "success"
    assert abs(outcome["result"]["value"] - exact) < tol


# ────────────────────────────────────────────────────────────────
# REGRESIÓN: funciones exponenciales
# ────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("method", METHODS)
def test_regresion_exp(method):
    """∫₀¹ e^x dx = e - 1"""
    exact = np.e - 1
    tol = TOL_REG[method]
    outcome = make_outcome(method, "exp(x)", [0, 1])
    assert outcome["status"] == "success"
    assert abs(outcome["result"]["value"] - exact) < tol


@pytest.mark.parametrize("method", METHODS)
def test_regresion_exp_neg(method):
    """∫₀¹ e^{-x} dx = 1 - e^{-1}"""
    exact = 1 - np.e**-1
    tol = TOL_REG[method]
    outcome = make_outcome(method, "exp(-x)", [0, 1])
    assert outcome["status"] == "success"
    assert abs(outcome["result"]["value"] - exact) < tol


# ────────────────────────────────────────────────────────────────
# REGRESIÓN: funciones a^x con a ∈ R
# ────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("method", METHODS)
def test_regresion_a_pow_x(method):
    """∫₀¹ 2^x dx = (2 - 1) / ln(2)"""
    exact = (2 - 1) / np.log(2)
    tol = TOL_REG[method]
    outcome = make_outcome(method, "2**x", [0, 1])
    assert outcome["status"] == "success"
    assert abs(outcome["result"]["value"] - exact) < tol


@pytest.mark.parametrize("method", METHODS)
def test_regresion_a_pow_x_decimal(method):
    """∫₀¹ 1.5^x dx = (1.5 - 1) / ln(1.5)"""
    exact = (1.5 - 1) / np.log(1.5)
    tol = TOL_REG[method]
    outcome = make_outcome(method, "1.5**x", [0, 1])
    assert outcome["status"] == "success"
    assert abs(outcome["result"]["value"] - exact) < tol


# ────────────────────────────────────────────────────────────────
# REGRESIÓN: funciones constantes
# ────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("method", METHODS)
def test_regresion_constante_5(method):
    """∫₀¹ 5 dx = 5"""
    tol = TOL_REG[method]
    outcome = make_outcome(method, "5", [0, 1])
    assert outcome["status"] == "success"
    assert abs(outcome["result"]["value"] - 5) < tol


@pytest.mark.parametrize("method", METHODS)
def test_regresion_constante_decimal(method):
    """∫₀¹ 0.25 dx = 0.25"""
    tol = TOL_REG[method]
    outcome = make_outcome(method, "0.25", [0, 1])
    assert outcome["status"] == "success"
    assert abs(outcome["result"]["value"] - 0.25) < tol
