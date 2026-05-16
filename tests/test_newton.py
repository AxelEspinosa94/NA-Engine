import pandas as pd
import pytest

from core.base_method import NumericalMethod
from core.exceptions import (
    ValidationError,
    MethodNotFoundError,
)


# ---------------------------------------------------------
# 1. Test: Full pipeline (table mode)
# ---------------------------------------------------------

def test_newton_full_pipeline_table_mode():
    df = pd.DataFrame({
        "x": [0, 1, 2],
        "f(x)": [1, 2, 5]   # f(x) = x^2 + 1
    })

    method = NumericalMethod(
        method="newton",
        input_data={
            "mode": "table",
            "data": df,
            "xk": 1.5
        }
    )

    assert method.validate_input() is True

    result = method.execute()

    # Expected: f(1.5) = 1.5^2 + 1 = 3.25
    assert abs(result["value"] - 3.25) < 1e-6
    assert "coefficients" in result
    assert "table" in result


# ---------------------------------------------------------
# 2. Test: Full pipeline (function mode)
# ---------------------------------------------------------

def test_newton_full_pipeline_function_mode():
    method = NumericalMethod(
        method="newton",
        input_data={
            "mode": "function",
            "data": "x**2 + 1",
            "interval": [0, 2],
            "step": 1,
            "xk": 1.5
        }
    )

    assert method.validate_input() is True

    result = method.execute()

    # Expected: f(1.5) = 3.25
    assert abs(result["value"] - 3.25) < 1e-6


# ---------------------------------------------------------
# 3. Test: Missing xk
# ---------------------------------------------------------

def test_newton_missing_xk():
    df = pd.DataFrame({"x": [0, 1], "f(x)": [1, 3]})

    method = NumericalMethod(
        method="newton",
        input_data={
            "mode": "table",
            "data": df
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()


# ---------------------------------------------------------
# 4. Test: Invalid mode
# ---------------------------------------------------------

def test_newton_invalid_mode():
    df = pd.DataFrame({"x": [0, 1], "f(x)": [1, 3]})

    method = NumericalMethod(
        method="newton",
        input_data={
            "mode": "invalid",
            "data": df,
            "xk": 1
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()


# ---------------------------------------------------------
# 5. Test: Method not found in catalog
# ---------------------------------------------------------

def test_newton_method_not_found():
    with pytest.raises(MethodNotFoundError):
        NumericalMethod(
            method="nonexistent_method",
            input_data={}
        )


# ---------------------------------------------------------
# 6. Test: DataFrame with wrong shape
# ---------------------------------------------------------

def test_newton_invalid_dataframe():
    df = pd.DataFrame({
        "x": [0, 1],
        "f(x)": [1, 3],
        "extra": [5, 6]
    })

    method = NumericalMethod(
        method="newton",
        input_data={
            "mode": "table",
            "data": df,
            "xk": 1
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()


# ---------------------------------------------------------
# 7. Test: Non-numeric xk
# ---------------------------------------------------------

def test_newton_non_numeric_xk():
    df = pd.DataFrame({"x": [0, 1], "f(x)": [1, 3]})

    method = NumericalMethod(
        method="newton",
        input_data={
            "mode": "table",
            "data": df,
            "xk": "hola"
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()
