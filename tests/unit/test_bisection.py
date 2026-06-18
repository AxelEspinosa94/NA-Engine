import numpy as np
import pytest
from core.base_method import NumericalMethod
from core.exceptions import ValidationError, ExecutionError


# ============================================================
# Convergencia básica
# ============================================================

def test_bisection_basic():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "x**2 - 2",
            "interval": [1, 2],
            "tol": 1e-6,
            "max_iter": 50,
            "calculation_mode": "bisection",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    assert abs(result["root"] - np.sqrt(2)) < 1e-6


# ============================================================
# No hay cambio de signo → falla en ejecución
# ============================================================

def test_bisection_no_sign_change():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "x**2 + 1",
            "interval": [-1, 1],
            "calculation_mode": "bisection",
        },
    )

    method.validate_input()

    response = method.execute()

    assert response["status"] == "error"
    assert response["error_type"] == "ExecutionError"



# ============================================================
# Intervalo invertido → falla en ejecución
# ============================================================

def test_bisection_reversed_interval():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "x**3 - 4*x + 1",
            "interval": [2, -2],
            "calculation_mode": "bisection",
        },
    )

    method.validate_input()

    response = method.execute()

    assert response["status"] == "error"
    assert response["error_type"] == "ExecutionError"


# ============================================================
# Intervalo inválido → falla en validación
# ============================================================

def test_bisection_invalid_interval():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "x - 1",
            "interval": [1],  # inválido
            "calculation_mode": "bisection",
        },
    )

    with pytest.raises(ValidationError):
        method.validate_input()


# ============================================================
# max_iter muy pequeño → falla en ejecución
# ============================================================

def test_bisection_max_iter():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "x**2 - 2",
            "interval": [1, 2],
            "tol": 1e-12,
            "max_iter": 1,
            "calculation_mode": "bisection",
        },
    )

    method.validate_input()

    response = method.execute()

    assert response["status"] == "error"
    assert response["error_type"] == "ExecutionError"


# ============================================================
# Tolerancia estricta
# ============================================================

def test_bisection_strict_tolerance():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "x**3 - x - 1",
            "interval": [1, 2],
            "tol": 1e-10,
            "max_iter": 100,
            "calculation_mode": "bisection",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    assert abs(result["root"] - 1.3247179572447458) < 1e-10


# ============================================================
# Raíz exacta en el borde → falla en ejecución
# ============================================================

def test_bisection_root_at_boundary():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "x - 3",
            "interval": [3, 10],
            "tol": 1e-6,
            "max_iter": 20,
            "calculation_mode": "bisection",
        },
    )

    method.validate_input()

    response = method.execute()

    assert response["status"] == "error"
    assert response["error_type"] == "ExecutionError"


# ============================================================
# Función oscilante
# ============================================================

def test_bisection_oscillatory():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "sin(x)",
            "interval": [3, 4],  # raíz en pi ≈ 3.14159
            "tol": 1e-6,
            "max_iter": 50,
            "calculation_mode": "bisection",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    assert abs(result["root"] - np.pi) < 1e-6


# ============================================================
# Función siempre positiva → falla en ejecución
# ============================================================

def test_bisection_always_positive():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "exp(x)",
            "interval": [-2, 2],
            "calculation_mode": "bisection",
        },
    )

    method.validate_input()

    response = method.execute()
    assert response["status"] == "error"
    assert response["error_type"] == "ExecutionError"
