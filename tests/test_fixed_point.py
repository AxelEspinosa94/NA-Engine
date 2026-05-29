import numpy as np
import pytest
from core.base_method import NumericalMethod
from core.exceptions import ValidationError


# ============================================================
# Convergencia
# ============================================================

def test_fixed_point_converges():
    """
    f(x) = x^2 - x - 1
    g(x) = sqrt(x + 1)
    Raíz ≈ 1.618...
    """
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "x**2 - x - 1",
            "g": "sqrt(x + 1)",
            "x0": 1.0,
            "tol": 1e-6,
            "max_iter": 50,
            "calculation_mode": "fixed_point",
        },
    )

    result = method.execute().get("result", {})
    assert abs(result["root"] - 1.6180339887) < 1e-6


# ============================================================
# Divergencia por |g'(x0)| >= 1
# ============================================================

def test_fixed_point_derivative_ge_1():
    """
    g(x) = 2x → g'(x) = 2 → diverge
    """
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "x",
            "g": "2*x",
            "x0": 1.0,
            "calculation_mode": "fixed_point",
        },
    )
    
    method.validate_input()

    response = method.execute()

    assert response["status"] == "error"
    assert response["error_type"] == "ExecutionError"


# ============================================================
# Divergencia por iteraciones máximas
# ============================================================

def test_fixed_point_max_iter_exceeded():
    """
    g(x) = cos(x) converge, pero con max_iter muy pequeño debe fallar.
    """
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "cos(x) - x",
                "g": "cos(x)",
                "x0": 1.0,
                "tol": 1e-12,
                "max_iter": 2,
                "calculation_mode": "fixed_point",
            },
        )
    method.validate_input()
    response = method.execute()
    assert response["status"] == "error"
    assert response["error_type"] == "ExecutionError"


# ============================================================
# Validación: falta g(x)
# ============================================================

def test_fixed_point_missing_g():
    with pytest.raises(ValidationError):
        NumericalMethod(
            method="nonlinear",
            input_data={
                "mode": "function",
                "function": "x**2 - 2",
                "x0": 1.0,
                "calculation_mode": "fixed_point",
            },
        ).validate_input()


# ============================================================
# Validación: falta x0
# ============================================================

def test_fixed_point_missing_x0():
    with pytest.raises(ValidationError):
        NumericalMethod(
            method="nonlinear",
            input_data={
                "mode": "function",
                "function": "x**2 - 2",
                "g": "sqrt(2)",
                "calculation_mode": "fixed_point",
            },
        ).validate_input()


# ============================================================
# NaN / infinito
# ============================================================

def test_fixed_point_nan():
    """
    g(x) = 1/(x-1) produce infinito en x0=1
    """
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "x - 1",
            "g": "1/(x - 1)",
            "x0": 1.0,
            "calculation_mode": "fixed_point",
        },
    )
    method.validate_input()
    response = method.execute()
    assert response["status"] == "error"
    assert response["error_type"] == "ExecutionError"
