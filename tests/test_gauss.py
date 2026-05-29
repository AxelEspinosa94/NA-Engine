import numpy as np
import pytest
from core.base_method import NumericalMethod
from core.exceptions import ValidationError


def test_gauss_basic_x2():
    """
    ∫₀¹ x² dx = 1/3
    """
    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "x**2",
            "interval": [0, 1],
            "n": 4,  # irrelevant for Gauss, but required by base class
            "gauss_points": 5,
            "calculation_mode": "gauss",
        },
    )

    result = method.execute().get("result", {})
    assert abs(result["value"] - 1/3) < 1e-12


def test_gauss_exp():
    """
    ∫₀¹ eˣ dx = e − 1
    """
    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "exp(x)",
            "interval": [0, 1],
            "n": 4,
            "gauss_points": 6,
            "calculation_mode": "gauss",
        },
    )

    result = method.execute().get("result", {})
    exact = np.e - 1
    assert abs(result["value"] - exact) < 1e-12


def test_gauss_sin():
    """
    ∫₀^π sin(x) dx = 2
    """
    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "sin(x)",
            "interval": [0, float(np.pi)],
            "n": 4,
            "gauss_points": 6,
            "calculation_mode": "gauss",
        },
    )

    result = method.execute().get("result", {})
    assert abs(result["value"] - 2) < 1e-9


def test_gauss_stress():
    """
    Stress test con varios números de puntos.
    """
    exact = np.e - 1

    for n_points in [2, 3, 5, 8, 10, 12]:
        method = NumericalMethod(
            method="integration",
            input_data={
                "mode": "function",
                "function": "exp(x)",
                "interval": [0, 1],
                "n": 4,
                "gauss_points": n_points,
                "calculation_mode": "gauss",
            },
        )

        result = method.execute().get("result", {})
        assert abs(result["value"] - exact) < 1e-3


def test_gauss_rejects_table_mode():
    """
    Gauss NO debe aceptar mode='table'.
    """
    with pytest.raises(ValidationError):
        NumericalMethod(
            method="integration",
            input_data={
                "mode": "table",
                "data": {"x": [0, 1], "f(x)": [0, 1]},
                "gauss_points": 4,
                "calculation_mode": "gauss",
            },
        ).validate_input()
