import numpy as np
import pytest

from core.base_method import NumericalMethod
from core.exceptions import ValidationError, ExecutionError


# ============================================================
# VALIDATION TESTS
# ============================================================

def test_missing_calculation_mode():
    method = NumericalMethod(
        method="numerical_derivative",
        input_data={
            "function": "x**2",
            "x": 1.0,
            "h": 1e-4,
        },
    )

    with pytest.raises(ValidationError):
        method.validate_input()


def test_invalid_function_string():
    method = NumericalMethod(
        method="numerical_derivative",
        input_data={
            "function": "",
            "x": 1.0,
            "h": 1e-4,
            "calculation_mode": "forward",
        },
    )

    with pytest.raises(ValidationError):
        method.validate_input()


def test_invalid_x_type():
    method = NumericalMethod(
        method="numerical_derivative",
        input_data={
            "function": "x**2",
            "x": "nope",
            "h": 1e-4,
            "calculation_mode": "forward",
        },
    )

    with pytest.raises(ValidationError):
        method.validate_input()


def test_invalid_h_type():
    method = NumericalMethod(
        method="numerical_derivative",
        input_data={
            "function": "x**2",
            "x": 1.0,
            "h": "nope",
            "calculation_mode": "forward",
        },
    )

    with pytest.raises(ValidationError):
        method.validate_input()


def test_negative_h():
    method = NumericalMethod(
        method="numerical_derivative",
        input_data={
            "function": "x**2",
            "x": 1.0,
            "h": -0.1,
            "calculation_mode": "forward",
        },
    )

    with pytest.raises(ValidationError):
        method.validate_input()


def test_partial_requires_y():
    method = NumericalMethod(
        method="numerical_derivative",
        input_data={
            "function": "x*y",
            "x": 1.0,
            "h": 1e-4,
            "calculation_mode": "partial_x",
        },
    )

    with pytest.raises(ValidationError):
        method.validate_input()


def test_invalid_richardson_order():
    method = NumericalMethod(
        method="numerical_derivative",
        input_data={
            "function": "x**2",
            "x": 1.0,
            "h": 1e-4,
            "calculation_mode": "richardson",
            "richardson_order": -2,
        },
    )

    with pytest.raises(ValidationError):
        method.validate_input()


# ============================================================
# EXECUTION TESTS
# ============================================================

def test_forward_derivative():
    method = NumericalMethod(
        method="numerical_derivative",
        input_data={
            "function": "x**2",
            "x": 2.0,
            "h": 1e-4,
            "calculation_mode": "forward",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    expected = 2 * 2.0  # derivative of x^2 at x=2
    assert np.allclose(result["derivative"], expected, atol=1e-4)


def test_backward_derivative():
    method = NumericalMethod(
        method="numerical_derivative",
        input_data={
            "function": "x**3",
            "x": 1.0,
            "h": 1e-4,
            "calculation_mode": "backward",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    expected = 3 * 1.0**2
    assert np.allclose(result["derivative"], expected, atol=5e-4)


def test_central_derivative():
    method = NumericalMethod(
        method="numerical_derivative",
        input_data={
            "function": "np.sin(x)",
            "x": np.pi / 4,
            "h": 1e-4,
            "calculation_mode": "central",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    expected = np.cos(np.pi / 4)
    assert np.allclose(result["derivative"], expected, atol=1e-6)


def test_richardson_derivative():
    method = NumericalMethod(
        method="numerical_derivative",
        input_data={
            "function": "np.exp(x)",
            "x": 1.0,
            "h": 1e-3,
            "calculation_mode": "richardson",
            "richardson_order": 2,
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    expected = np.exp(1.0)
    assert np.allclose(result["derivative"], expected, atol=1e-6)


def test_second_forward():
    method = NumericalMethod(
        method="numerical_derivative",
        input_data={
            "function": "x**3",
            "x": 2.0,
            "h": 1e-4,
            "calculation_mode": "second_forward",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    expected = 6 * 2.0  # second derivative of x^3
    assert np.allclose(result["second_derivative"], expected, atol=1e-3)


def test_second_central():
    method = NumericalMethod(
        method="numerical_derivative",
        input_data={
            "function": "np.sin(x)",
            "x": np.pi / 3,
            "h": 1e-4,
            "calculation_mode": "second_central",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    expected = -np.sin(np.pi / 3)
    assert np.allclose(result["second_derivative"], expected, atol=1e-4)


def test_third_forward():
    method = NumericalMethod(
        method="numerical_derivative",
        input_data={
            "function": "x**4",
            "x": 1.0,
            "h": 1e-4,
            "calculation_mode": "third_forward",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    expected = 24 * 1.0  # third derivative of x^4
    assert np.allclose(result["third_derivative"], expected, atol=1e-2)


def test_partial_x():
    method = NumericalMethod(
        method="numerical_derivative",
        input_data={
            "function": "x*y",
            "x": 3.0,
            "y": 4.0,
            "h": 1e-4,
            "calculation_mode": "partial_x",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    expected = 4.0  # ∂/∂x (x*y) = y
    assert np.allclose(result["partial_x"], expected, atol=1e-6)


def test_partial_y():
    method = NumericalMethod(
        method="numerical_derivative",
        input_data={
            "function": "x*y",
            "x": 3.0,
            "y": 4.0,
            "h": 1e-4,
            "calculation_mode": "partial_y",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    expected = 3.0  # ∂/∂y (x*y) = x
    assert np.allclose(result["partial_y"], expected, atol=1e-6)
