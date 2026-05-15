import pandas as pd
import pytest

from core.base_method import NumericalMethod
from core.exceptions import (
    ValidationError,
    MethodNotFoundError,
    ExecutionError,
)


# ---------------------------
# 1. Test: Registry + Abstract Class + Full Pipeline
# ---------------------------

def test_lagrange_full_pipeline_table_mode():
    df = pd.DataFrame({
        "x": [0, 1],
        "f(x)": [1, 3]
    })

    method = NumericalMethod(
        method="lagrange",
        input_data={
            "mode": "table",
            "data": df,
            "xk": 0.5
        }
    )

    assert method.validate_input() is True

    result = method.execute()
    assert abs(result["value"] - 2.0) < 1e-6
    assert "expression" in result
    assert "table" in result


# ---------------------------
# 2. Test: Function mode
# ---------------------------

def test_lagrange_full_pipeline_function_mode():
    method = NumericalMethod(
        method="lagrange",
        input_data={
            "mode": "function",
            "data": "x**2",
            "interval": [0, 2],
            "step": 1,
            "xk": 1.5
        }
    )

    assert method.validate_input() is True

    result = method.execute()
    assert isinstance(result["value"], float)


# ---------------------------
# 3. Test: Missing xk
# ---------------------------

def test_lagrange_missing_xk():
    df = pd.DataFrame({"x": [0, 1], "f(x)": [1, 3]})

    method = NumericalMethod(
        method="lagrange",
        input_data={
            "mode": "table",
            "data": df
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()


# ---------------------------
# 4. Test: Invalid mode
# ---------------------------

def test_lagrange_invalid_mode():
    df = pd.DataFrame({"x": [0, 1], "f(x)": [1, 3]})

    method = NumericalMethod(
        method="lagrange",
        input_data={
            "mode": "invalid",
            "data": df,
            "xk": 1
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()


# ---------------------------
# 5. Test: Method not found in catalog
# ---------------------------

def test_method_not_found():
    with pytest.raises(MethodNotFoundError):
        NumericalMethod(
            method="nonexistent_method",
            input_data={}
        )


# ---------------------------
# 6. Test: DataFrame with wrong shape
# ---------------------------

def test_lagrange_invalid_dataframe():
    df = pd.DataFrame({
        "x": [0, 1],
        "f(x)": [1, 3],
        "extra": [5, 6]
    })

    method = NumericalMethod(
        method="lagrange",
        input_data={
            "mode": "table",
            "data": df,
            "xk": 1
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()
