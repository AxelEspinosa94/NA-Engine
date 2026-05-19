import numpy as np
import pytest
from core.base_method import NumericalMethod
from core.exceptions import ValidationError


# ============================================================
# TRAPECIO SIMPLE
# ============================================================

def test_trapezoid_simple_x2():
    """
    ∫₀¹ x² dx ≈ 0.5 * (f(0) + f(1)) = 0.5
    """
    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "x**2",
            "interval": [0, 1],
            "n": 1,  # trapecio simple requiere n = 1
            "calculation_mode": "trapezoid_simple",
        },
    )

    result = method.execute()
    assert abs(result["value"] - 0.5) < 1e-12


def test_trapezoid_simple_rejects_wrong_n():
    """
    trapecio simple debe fallar si n != 1
    """
    with pytest.raises(ValidationError):
        NumericalMethod(
            method="integration",
            input_data={
                "mode": "function",
                "function": "x**2",
                "interval": [0, 1],
                "n": 4,
                "calculation_mode": "trapezoid_simple",
            },
        ).validate_input()


# ============================================================
# TRAPECIO COMPUESTO
# ============================================================

def test_trapezoid_composite_x2():
    """
    ∫₀¹ x² dx = 1/3
    """
    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "x**2",
            "interval": [0, 1],
            "n": 10,
            "calculation_mode": "trapezoid_composite",
        },
    )

    result = method.execute()
    assert abs(result["value"] - 1/3) < 1.7e-3  # trapecio compuesto es O(h^2)


# ============================================================
# SIMPSON 1/3
# ============================================================

def test_simpson_1_3_x2():
    """
    Simpson 1/3 es exacto para polinomios hasta grado 3.
    ∫₀¹ x² dx = 1/3
    """
    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "x**2",
            "interval": [0, 1],
            "n": 6,  # n par
            "calculation_mode": "simpson_1_3",
        },
    )

    result = method.execute()
    assert abs(result["value"] - 1/3) < 1e-12


def test_simpson_1_3_rejects_odd_n():
    """
    Simpson 1/3 requiere n par.
    """
    with pytest.raises(ValidationError):
        NumericalMethod(
            method="integration",
            input_data={
                "mode": "function",
                "function": "x**2",
                "interval": [0, 1],
                "n": 5,
                "calculation_mode": "simpson_1_3",
            },
        ).validate_input()


# ============================================================
# SIMPSON 3/8
# ============================================================

def test_simpson_3_8_x2():
    """
    Simpson 3/8 es exacto para polinomios hasta grado 3.
    ∫₀¹ x² dx = 1/3
    """
    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "x**2",
            "interval": [0, 1],
            "n": 6,  # múltiplo de 3
            "calculation_mode": "simpson_3_8",
        },
    )

    result = method.execute()
    assert abs(result["value"] - 1/3) < 1e-12


def test_simpson_3_8_rejects_non_multiple_of_3():
    """
    Simpson 3/8 requiere n múltiplo de 3.
    """
    with pytest.raises(ValidationError):
        NumericalMethod(
            method="integration",
            input_data={
                "mode": "function",
                "function": "x**2",
                "interval": [0, 1],
                "n": 5,
                "calculation_mode": "simpson_3_8",
            },
        ).validate_input()
