import numpy as np
import pytest
from core.base_method import NumericalMethod
from core.exceptions import ValidationError, ExecutionError


# ============================================================
# Convergencia básica
# ============================================================

def test_false_position_basic():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "x**2 - 2",
            "interval": [1, 2],
            "tol": 1e-6,
            "max_iter": 50,
            "calculation_mode": "false_position",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    assert abs(result["root"] - np.sqrt(2)) < 1e-6


# ============================================================
# No hay cambio de signo → falla en ejecución
# ============================================================

def test_false_position_no_sign_change():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "x**2 + 1",
            "interval": [-1, 1],
            "calculation_mode": "false_position",
        },
    )

    method.validate_input()
    response = method.execute()
    assert response["status"] == "error"
    assert response["error_type"] == "ExecutionError"


# ============================================================
# Intervalo inválido → falla en validación
# ============================================================

def test_false_position_invalid_interval():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "x - 1",
            "interval": [1],  # inválido
            "calculation_mode": "false_position",
        },
    )

    with pytest.raises(ValidationError):
        method.validate_input()


# ============================================================
# max_iter insuficiente → falla en ejecución
# ============================================================

def test_false_position_max_iter_exceeded():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "x**3 - x - 1",
            "interval": [1, 2],
            "tol": 1e-12,
            "max_iter": 1,
            "calculation_mode": "false_position",
        },
    )

    method.validate_input()
    response = method.execute()
    assert response["status"] == "error"
    assert response["error_type"] == "ExecutionError"


# ============================================================
# Función oscilante
# ============================================================

def test_false_position_oscillatory():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "sin(x)",
            "interval": [3, 4],  # raíz en pi
            "tol": 1e-6,
            "max_iter": 50,
            "calculation_mode": "false_position",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    assert abs(result["root"] - np.pi) < 1e-6


# ============================================================
# Función siempre positiva → falla en ejecución
# ============================================================

def test_false_position_always_positive():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "exp(x)",
            "interval": [-2, 2],
            "calculation_mode": "false_position",
        },
    )

    method.validate_input()
    response = method.execute()
    assert response["status"] == "error"
    assert response["error_type"] == "ExecutionError"
