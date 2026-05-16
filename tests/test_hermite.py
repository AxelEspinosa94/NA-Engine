import pandas as pd
import numpy as np
import pytest

from core.base_method import NumericalMethod
from core.exceptions import ValidationError


# ---------------------------------------------------------
# 1. Hermite exacto: f(x) = x^2  → Hermite coincide EXACTO
# ---------------------------------------------------------

def test_hermite_exact_quadratic():
    df = pd.DataFrame({
        "x": [0, 1, 2],
        "f(x)": [0**2, 1**2, 2**2],
        "f'(x)": [0, 2, 4]
    })

    method = NumericalMethod(
        method="hermite",
        input_data={
            "mode": "table",
            "data": df,
            "xk": 1.5
        }
    )

    assert method.validate_input() is True

    result = method.execute()

    # f(1.5) = 2.25
    assert abs(result["value"] - 2.25) < 1e-6


# ---------------------------------------------------------
# 2. Hermite general (tabla)
# ---------------------------------------------------------

def test_hermite_general_case():
    df = pd.DataFrame({
        "x": [0, 1],
        "f(x)": [1, 3],
        "f'(x)": [0, 2]
    })

    method = NumericalMethod(
        method="hermite",
        input_data={
            "mode": "table",
            "data": df,
            "xk": 0.5
        }
    )

    assert method.validate_input() is True

    result = method.execute()

    # Valor esperado calculado manualmente
    expected = 1.75
    assert abs(result["value"] - expected) < 1e-6


# ---------------------------------------------------------
# 3. Hermite modo function (derivada automática)
# ---------------------------------------------------------

def test_hermite_function_mode():
    method = NumericalMethod(
        method="hermite",
        input_data={
            "mode": "function",
            "function": "x**3",
            "interval": [0, 2],
            "step": 1,
            "xk": 1.5
        }
    )

    assert method.validate_input() is True

    result = method.execute()

    # f(1.5) = 3.375
    assert abs(result["value"] - 3.375) < 1e-3


# ---------------------------------------------------------
# 4. x no estrictamente creciente
# ---------------------------------------------------------

def test_hermite_x_not_increasing():
    df = pd.DataFrame({
        "x": [0, 2, 1],
        "f(x)": [1, 3, 2],
        "f'(x)": [0, 1, 2]
    })

    method = NumericalMethod(
        method="hermite",
        input_data={
            "mode": "table",
            "data": df,
            "xk": 1
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()


# ---------------------------------------------------------
# 5. NaNs en la tabla
# ---------------------------------------------------------

def test_hermite_with_nans():
    df = pd.DataFrame({
        "x": [0, 1],
        "f(x)": [1, np.nan],
        "f'(x)": [0, 2]
    })

    method = NumericalMethod(
        method="hermite",
        input_data={
            "mode": "table",
            "data": df,
            "xk": 0.5
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()


# ---------------------------------------------------------
# 6. Falta la columna de derivada
# ---------------------------------------------------------

def test_hermite_missing_derivative_column():
    df = pd.DataFrame({
        "x": [0, 1],
        "f(x)": [1, 3]
    })

    method = NumericalMethod(
        method="hermite",
        input_data={
            "mode": "table",
            "data": df,
            "xk": 0.5
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()


# ---------------------------------------------------------
# 7. Modo inválido
# ---------------------------------------------------------

def test_hermite_invalid_mode():
    df = pd.DataFrame({
        "x": [0, 1],
        "f(x)": [1, 3],
        "f'(x)": [0, 2]
    })

    method = NumericalMethod(
        method="hermite",
        input_data={
            "mode": "invalid",
            "data": df,
            "xk": 0.5
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()

