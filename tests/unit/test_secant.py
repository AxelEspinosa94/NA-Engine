import numpy as np
import pytest
from core.base_method import NumericalMethod
from core.exceptions import ValidationError, ExecutionError


# ============================================================
# Convergencia básica
# ============================================================

def test_secant_basic():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "x**2 - 2",
            "x0": 1.0,
            "x1": 2.0,
            "tol": 1e-6,
            "max_iter": 50,
            "calculation_mode": "secant",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    assert abs(result["root"] - np.sqrt(2)) < 1e-6


# ============================================================
# Denominador cero → falla en ejecución
# ============================================================

def test_secant_zero_denominator():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "x**3",
            "x0": 0.0,
            "x1": 0.0,
            "calculation_mode": "secant",
        },
    )

    method.validate_input()
    response = method.execute()
    assert response["status"] == "error"
    assert response["error_type"] == "ExecutionError"


# ============================================================
# Divergencia → falla en ejecución
# ============================================================

def test_secant_diverges():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "exp(x)",
            "x0": -2,
            "x1": -1,
            "tol": 1e-8,
            "max_iter": 5,
            "calculation_mode": "secant",
        },
    )

    method.validate_input()
    response = method.execute()
    assert response["status"] == "error"
    assert response["error_type"] == "ExecutionError"


# ============================================================
# max_iter insuficiente → falla en ejecución
# ============================================================

def test_secant_max_iter_exceeded():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "cos(x) - x",
            "x0": 0.0,
            "x1": 1.0,
            "tol": 1e-12,
            "max_iter": 1,
            "calculation_mode": "secant",
        },
    )

    method.validate_input()
    response = method.execute()
    assert response["status"] == "error"
    assert response["error_type"] == "ExecutionError"


# ============================================================
# Validación: falta x0 o x1
# ============================================================

def test_secant_missing_x0_x1():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "x**2 - 2",
            "calculation_mode": "secant",
        },
    )

    with pytest.raises(ValidationError):
        method.validate_input()
