import numpy as np
import pandas as pd
import pytest

from core.base_method import NumericalMethod
from core.exceptions import ValidationError


def test_romberg_x2():
    """
    ∫₀¹ x² dx = 1/3
    """
    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "x**2",
            "interval": [0, 1],
            "n": 6,
            "calculation_mode": "romberg",
        },
    )

    result = method.execute()
    assert abs(result["value"] - 1/3) < 1e-10


def test_romberg_sin():
    """
    ∫₀^π sin(x) dx = 2
    """
    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "sin(x)",
            "interval": [0, float(np.pi)],
            "n": 6,
            "calculation_mode": "romberg",
        },
    )

    result = method.execute()
    assert abs(result["value"] - 2) < 1e-10


def test_romberg_exp():
    """
    ∫₀¹ eˣ dx = e − 1
    """
    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "exp(x)",
            "interval": [0, 1],
            "n": 6,
            "calculation_mode": "romberg",
        },
    )

    result = method.execute()
    exact = np.e - 1
    assert abs(result["value"] - exact) < 1e-10


def test_romberg_higher_n_stable():
    """
    Mismo integral que x², pero con n más grande para ver estabilidad.
    """
    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "x**2",
            "interval": [0, 1],
            "n": 8,
            "calculation_mode": "romberg",
        },
    )

    result = method.execute()
    assert abs(result["value"] - 1/3) < 1e-12


def test_romberg_rejects_table_mode():
    """
    Romberg NO debe aceptar mode='table'.
    """
    df = pd.DataFrame({"x": [0, 1], "f(x)": [0, 1]})

    with pytest.raises(ValidationError):
        NumericalMethod(
            method="integration",
            input_data={
                "mode": "table",
                "data": df,
                "calculation_mode": "romberg",
            },
        ).validate_input()
