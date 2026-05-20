import numpy as np
import pytest
from core.base_method import NumericalMethod
from core.exceptions import ValidationError, ExecutionError


# ============================================================
# Convergencia básica
# ============================================================

def test_newton_converges_basic():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "x**2 - 2",
            "x0": 1.5,
            "tol": 1e-8,
            "max_iter": 20,
            "calculation_mode": "newton",
        },
    )

    # Primero validamos
    method.validate_input()

    # Luego ejecutamos
    result = method.execute()

    assert abs(result["root"] - np.sqrt(2)) < 1e-8


# ============================================================
# Convergencia con raíz múltiple
# ============================================================

def test_newton_multiple_root():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "(x - 1)**3",
            "x0": 0.5,
            "tol": 1e-6,
            "max_iter": 50,
            "calculation_mode": "newton",
        },
    )

    method.validate_input()
    result = method.execute()

    assert abs(result["root"] - 1) < 1.8e-6


# ============================================================
# Derivada cero → debe fallar en ejecución
# ============================================================

def test_newton_derivative_zero():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "x**3",
            "x0": 0.0,
            "calculation_mode": "newton",
        },
    )

    # Validación pasa (x0 existe, function existe)
    method.validate_input()

    # La falla ocurre en ejecución
    with pytest.raises(ExecutionError):
        method.execute()


# ============================================================
# Divergencia → debe fallar en ejecución
# ============================================================

def test_newton_diverges():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "x**(1/3)",
            "x0": 10.0,
            "tol": 1e-8,
            "max_iter": 10,
            "calculation_mode": "newton",
        },
    )

    method.validate_input()

    with pytest.raises(ExecutionError):
        method.execute()


# ============================================================
# max_iter insuficiente → debe fallar en ejecución
# ============================================================

def test_newton_max_iter_exceeded():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "cos(x) - x",
            "x0": 1.0,
            "tol": 1e-12,
            "max_iter": 1,
            "calculation_mode": "newton",
        },
    )

    method.validate_input()

    with pytest.raises(ExecutionError):
        method.execute()


# ============================================================
# NaN / infinito → debe fallar en ejecución
# ============================================================

def test_newton_nan():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "1/(x - 1)",
            "x0": 1.0,
            "calculation_mode": "newton",
        },
    )

    method.validate_input()

    with pytest.raises(ExecutionError):
        method.execute()


# ============================================================
# Validación: falta x0
# ============================================================

def test_newton_missing_x0():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "x**2 - 2",
            "calculation_mode": "newton",
        },
    )

    with pytest.raises(ValidationError):
        method.validate_input()
