import numpy as np
import pytest

from core.base_method import NumericalMethod
from core.exceptions import ConstructionError, ValidationError

# ============================================================
# CONSTRUCTOR ERRORS
# ============================================================


def test_clenshaw_constructor_rejects_missing_function():
    """
    Constructor must reject missing 'function' key.
    """
    with pytest.raises(ConstructionError):
        NumericalMethod(
            method="integration",
            input_data={
                "mode": "function",
                "interval": [0, 1],
                "n": 10,
                "calculation_mode": "clenshaw_curtis",
            },
        )


def test_clenshaw_constructor_rejects_bad_interval():
    """
    Constructor must reject malformed interval.
    """
    with pytest.raises(ConstructionError):
        NumericalMethod(
            method="integration",
            input_data={
                "mode": "function",
                "function": "x**2",
                "interval": [1],  # malformed
                "n": 10,
                "calculation_mode": "clenshaw_curtis",
            },
        )


def test_clenshaw_constructor_rejects_non_numeric_n():
    """
    Constructor must reject non-numeric n.
    """
    with pytest.raises(ConstructionError):
        NumericalMethod(
            method="integration",
            input_data={
                "mode": "function",
                "function": "x**2",
                "interval": [0, 1],
                "n": "hola",
                "calculation_mode": "clenshaw_curtis",
            },
        )


def test_clenshaw_rejects_negative_n():
    """
    n must be positive.
    """
    with pytest.raises(ConstructionError):
        NumericalMethod(
            method="integration",
            input_data={
                "mode": "function",
                "function": "x**2",
                "interval": [0, 1],
                "n": -2,
                "calculation_mode": "clenshaw_curtis",
            },
        )


# ============================================================
# VALIDATION ERRORS
# ============================================================


def test_clenshaw_rejects_odd_n():
    """
    Clenshaw–Curtis requires n even.
    """
    with pytest.raises(ValidationError):
        NumericalMethod(
            method="integration",
            input_data={
                "mode": "function",
                "function": "x**2",
                "interval": [0, 1],
                "n": 5,  # odd → invalid
                "calculation_mode": "clenshaw_curtis",
            },
        ).validate_input()


# ============================================================
# BASIC INTEGRAL TESTS
# ============================================================


def test_clenshaw_x2_0_1():
    """
    ∫₀¹ x² dx = 1/3
    CC should be nearly exact for polynomials.
    """
    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "x**2",
            "interval": [0, 1],
            "n": 10,  # even
            "calculation_mode": "clenshaw_curtis",
        },
    )

    result = method.execute().get("result", {})
    assert abs(result["value"] - 1 / 3) < 1e-12


def test_clenshaw_x3_0_1():
    """
    ∫₀¹ x³ dx = 1/4
    CC is exact for cubic polynomials.
    """
    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "x**3",
            "interval": [0, 1],
            "n": 12,
            "calculation_mode": "clenshaw_curtis",
        },
    )

    result = method.execute().get("result", {})
    assert abs(result["value"] - 1 / 4) < 1e-12


# ============================================================
# SMOOTH FUNCTION TESTS
# ============================================================


def test_clenshaw_exp_0_1():
    """
    ∫₀¹ e^x dx = e - 1
    CC converges spectrally for smooth functions.
    """
    exact = np.e - 1

    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "exp(x)",
            "interval": [0, 1],
            "n": 20,
            "calculation_mode": "clenshaw_curtis",
        },
    )

    result = method.execute().get("result", {})
    assert abs(result["value"] - exact) < 1e-10


def test_clenshaw_sin_0_pi():
    """
    ∫₀^π sin(x) dx = 2
    """
    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "sin(x)",
            "interval": [0, np.pi],
            "n": 20,
            "calculation_mode": "clenshaw_curtis",
        },
    )

    result = method.execute().get("result", {})
    assert abs(result["value"] - 2) < 1e-10


# ============================================================
# EDGE CASES
# ============================================================


def test_clenshaw_constant_function():
    """
    ∫₀¹ 5 dx = 5
    """
    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "5",
            "interval": [0, 1],
            "n": 8,
            "calculation_mode": "clenshaw_curtis",
        },
    )

    result = method.execute().get("result", {})
    assert abs(result["value"] - 5) < 1e-12


def test_clenshaw_linear_function():
    """
    ∫₀¹ x dx = 1/2
    """
    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "x",
            "interval": [0, 1],
            "n": 8,
            "calculation_mode": "clenshaw_curtis",
        },
    )

    result = method.execute().get("result", {})
    assert abs(result["value"] - 0.5) < 1e-12
