import pandas as pd
import numpy as np
import pytest

from core.base_method import NumericalMethod
from core.exceptions import ValidationError


# ---------------------------------------------------------
# 1. Test: Spline cúbico natural en una función suave
#    f(x) = x^3  → el spline debe reproducir EXACTAMENTE
# ---------------------------------------------------------

def test_spline_cubic_exact_function():
    df = pd.DataFrame({
        "x": [0, 1, 2, 3],
        "f(x)": [0**3, 1**3, 2**3, 3**3]
    })

    method = NumericalMethod(
        method="spline_cubic",
        input_data={
            "mode": "table",
            "data": df,
            "xk": 1.5
        }
    )

    assert method.validate_input() is True

    result = method.execute()

    # f(1.5) = 3.375
    assert abs(result["value"] - 3.15) < 1e-6


# ---------------------------------------------------------
# 2. Test: Spline cúbico natural en datos generales
# ---------------------------------------------------------

def test_spline_cubic_general_case():
    df = pd.DataFrame({
        "x": [0, 1, 2],
        "f(x)": [1, 3, 2]
    })

    method = NumericalMethod(
        method="spline_cubic",
        input_data={
            "mode": "table",
            "data": df,
            "xk": 0.5
        }
    )

    assert method.validate_input() is True

    result = method.execute()

    # Valor esperado aproximado (calculado con spline cúbico natural)
    expected = 2.28125
    assert abs(result["value"] - expected) < 1e-4


# ---------------------------------------------------------
# 3. Test: x no estrictamente creciente
# ---------------------------------------------------------

def test_spline_cubic_x_not_increasing():
    df = pd.DataFrame({
        "x": [0, 2, 1],
        "f(x)": [1, 3, 2]
    })

    method = NumericalMethod(
        method="spline_cubic",
        input_data={
            "mode": "table",
            "data": df,
            "xk": 1
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()


# ---------------------------------------------------------
# 4. Test: Menos de 3 puntos
# ---------------------------------------------------------

def test_spline_cubic_too_few_points():
    df = pd.DataFrame({
        "x": [0, 1],
        "f(x)": [1, 3]
    })

    method = NumericalMethod(
        method="spline_cubic",
        input_data={
            "mode": "table",
            "data": df,
            "xk": 0.5
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()


# ---------------------------------------------------------
# 5. Test: NaNs en la tabla
# ---------------------------------------------------------

def test_spline_cubic_with_nans():
    df = pd.DataFrame({
        "x": [0, 1, 2],
        "f(x)": [1, np.nan, 3]
    })

    method = NumericalMethod(
        method="spline_cubic",
        input_data={
            "mode": "table",
            "data": df,
            "xk": 1
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()
