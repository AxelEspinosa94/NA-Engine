import pytest

from core.base_method import NumericalMethod
from core.exceptions import ConstructionError, ValidationError

# ============================================================
# MONTE CARLO 1D
# ============================================================


def test_montecarlo_x2_0_1():
    """
    ∫₀¹ x² dx = 1/3
    """

    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "x**2",
            "bounds": [0, 1],
            "n": 10000,
            "calculation_mode": "montecarlo",
        },
    )

    result = method.execute().get("result", {})

    assert abs(result["value"] - 1 / 3) < 5e-3


def test_montecarlo_constant_function():
    """
    ∫₀¹ 5 dx = 5
    """

    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "5",
            "bounds": [0, 1],
            "n": 1000,
            "calculation_mode": "montecarlo",
        },
    )

    result = method.execute().get("result", {})

    assert abs(result["value"] - 5.0) < 5e-3


def test_montecarlo_linear_function():
    """
    ∫₀¹ x dx = 1/2
    """

    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "x",
            "bounds": [0, 1],
            "n": 12000,
            "calculation_mode": "montecarlo",
        },
    )

    result = method.execute().get("result", {})

    assert abs(result["value"] - 0.5) < 5e-3


# ============================================================
# MONTE CARLO ND
# ============================================================


def test_montecarlo_2d_linear():
    """
    ∫∫ (x0 + x1)
    sobre [0,1]×[0,1]

    = 1
    """

    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "x0 + x1",
            "bounds": [
                [0, 1],
                [0, 1],
            ],
            "n": 10000,
            "calculation_mode": "montecarlo",
        },
    )

    result = method.execute().get("result", {})

    assert abs(result["value"] - 1.0) < 1e-2


def test_montecarlo_3d_linear():
    """
    ∭ (x0 + x1 + x2) sobre [0,1]^3 = 3/2
    """

    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "x0 + x1 + x2",
            "bounds": [
                [0, 1],
                [0, 1],
                [0, 1],
            ],
            "n": 1000,
            "calculation_mode": "montecarlo",
        },
    )

    result = method.execute().get("result", {})

    assert abs(result["value"] - 1.5) < 2e-2


# ============================================================
# VALIDATIONS
# ============================================================


def test_montecarlo_rejects_empty_function():

    with pytest.raises(ConstructionError):

        NumericalMethod(
            method="integration",
            input_data={
                "mode": "function",
                "function": "",
                "bounds": [0, 1],
                "n": 10,
                "calculation_mode": "montecarlo",
            },
        )


def test_montecarlo_rejects_empty_bounds():

    with pytest.raises(ConstructionError):

        NumericalMethod(
            method="integration",
            input_data={
                "mode": "function",
                "function": "x",
                "bounds": [],
                "n": 10,
                "calculation_mode": "montecarlo",
            },
        )


def test_montecarlo_rejects_invalid_interval_length():

    with pytest.raises(ConstructionError):

        NumericalMethod(
            method="integration",
            input_data={
                "mode": "function",
                "function": "x0+x1",
                "bounds": [
                    [0, 1],
                    [2],
                    [3, 4],
                ],
                "n": 10,
                "calculation_mode": "montecarlo",
            },
        )


def test_montecarlo_rejects_reversed_interval():

    with pytest.raises(ConstructionError):

        NumericalMethod(
            method="integration",
            input_data={
                "mode": "function",
                "function": "x",
                "bounds": [1, 0],
                "n": 10,
                "calculation_mode": "montecarlo",
            },
        )


def test_montecarlo_rejects_non_positive_n():

    with pytest.raises(ConstructionError):
        NumericalMethod(
            method="integration",
            input_data={
                "mode": "function",
                "function": "x",
                "bounds": [0, 1],
                "n": 0,
                "calculation_mode": "montecarlo",
            },
        )
