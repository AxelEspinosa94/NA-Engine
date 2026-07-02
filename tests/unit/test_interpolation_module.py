import pandas as pd
import numpy as np
import pytest

from core.base_method import NumericalMethod
from core.exceptions import ValidationError, ConstructionError, ExecutionError


# ---------------------------------------------------------
# 1. BASIC CONSTRUCTOR TESTS
# ---------------------------------------------------------

def test_constructor_table_lagrange():
    df = pd.DataFrame({"x": [0, 1, 2], "f(x)": [1, 2, 3]})

    method = NumericalMethod(
        method="interpolation",
        input_data={
            "mode": "table",
            "calculation_mode": "lagrange",
            "data": df,
            "xk": 1.5
        }
    )

    method.validate_input()
    result = method.execute()

    assert result["status"] == "success"
    assert "value" in result["result"]


def test_constructor_function_lagrange():
    method = NumericalMethod(
        method="interpolation",
        input_data={
            "mode": "function",
            "calculation_mode": "lagrange",
            "data": "x**2",
            "interval": [0, 2],
            "step": 1,
            "xk": 1.5
        }
    )

    method.validate_input()
    result = method.execute()

    assert result["status"] == "success"


# ---------------------------------------------------------
# 2. VALIDATOR TESTS
# ---------------------------------------------------------

def test_validator_invalid_mode():
    with pytest.raises(ConstructionError):
        NumericalMethod(
            method="interpolation",
            input_data={
                "mode": "invalid",
                "calculation_mode": "lagrange",
                "data": None,
                "xk": 1
            }
        )


def test_validator_missing_xk():
    df = pd.DataFrame({"x": [0, 1], "f(x)": [1, 2]})

    with pytest.raises(ValidationError):
        NumericalMethod(
            method="interpolation",
            input_data={
                "mode": "table",
                "calculation_mode": "lagrange",
                "data": df
            }
        ).validate_input()


def test_validator_hermite_table_wrong_columns():
    df = pd.DataFrame({"x": [0, 1], "f(x)": [1, 2]})

    with pytest.raises(ConstructionError):
        NumericalMethod(
            method="interpolation",
            input_data={
                "mode": "table",
                "calculation_mode": "hermite",
                "data": df,
                "xk": 0.5
            }
        )


# ---------------------------------------------------------
# 3. EXECUTOR TESTS
# ---------------------------------------------------------

def test_lagrange_executor():
    df = pd.DataFrame({"x": [0, 1, 2], "f(x)": [1, 2, 5]})

    method = NumericalMethod(
        method="interpolation",
        input_data={
            "mode": "table",
            "calculation_mode": "lagrange",
            "data": df,
            "xk": 1
        }
    )

    method.validate_input()
    result = method.execute()

    assert result["status"] == "success"
    assert abs(result["result"]["value"] - 2) < 1e-6


def test_newton_executor():
    df = pd.DataFrame({"x": [0, 1, 2], "f(x)": [1, 2, 5]})

    method = NumericalMethod(
        method="interpolation",
        input_data={
            "mode": "table",
            "calculation_mode": "newton",
            "data": df,
            "xk": 1
        }
    )

    method.validate_input()
    result = method.execute()

    assert result["status"] == "success"
    assert abs(result["result"]["value"] - 2) < 1e-6


def test_spline_executor():
    df = pd.DataFrame({"x": [0, 1, 2], "f(x)": [1, 2, 5]})

    method = NumericalMethod(
        method="interpolation",
        input_data={
            "mode": "table",
            "calculation_mode": "spline_cubic",
            "data": df,
            "xk": 1
        }
    )

    method.validate_input()
    result = method.execute()

    assert result["status"] == "success"


def test_hermite_executor():
    df = pd.DataFrame({
        "x": [0, 1],
        "f(x)": [1, 2],
        "f'(x)": [0, 1]
    })

    method = NumericalMethod(
        method="interpolation",
        input_data={
            "mode": "table",
            "calculation_mode": "hermite",
            "data": df,
            "xk": 0.5
        }
    )

    method.validate_input()
    result = method.execute()

    assert result["status"] == "success"
    assert "Q" in result["result"]
    assert "z" in result["result"]


# ---------------------------------------------------------
# 4. ERROR HANDLING TESTS
# ---------------------------------------------------------

def test_invalid_function_expression():
    with pytest.raises(ConstructionError):
        NumericalMethod(
            method="interpolation",
            input_data={
                "mode": "function",
                "calculation_mode": "lagrange",
                "data": "x***2",
                "interval": [0, 1],
                "step": 0.1,
                "xk": 0.5
            }
        )


def test_spline_invalid_df_columns():
    df = pd.DataFrame({"x": [0, 1, 2], "y": [1, 2, 3], "z": [0, 0, 0]})

    with pytest.raises(ConstructionError):
        NumericalMethod(
            method="interpolation",
            input_data={
                "mode": "table",
                "calculation_mode": "spline_cubic",
                "data": df,
                "xk": 1
            }
        )
