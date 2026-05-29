import numpy as np
import pytest

from core.base_method import NumericalMethod
from core.exceptions import ValidationError, ExecutionError


# ============================================================
# VALIDATION TESTS
# ============================================================

def test_missing_calculation_mode():
    method = NumericalMethod(
        method="ode",
        input_data={
            "function": "x + y",
            "x0": 0,
            "y0": 1,
            "x_end": 1,
            "h": 0.1,
        },
    )
    with pytest.raises(ValidationError):
        method.validate_input()


def test_invalid_function():
    method = NumericalMethod(
        method="ode",
        input_data={
            "function": 123,
            "x0": 0,
            "y0": 1,
            "x_end": 1,
            "h": 0.1,
            "calculation_mode": "euler",
        },
    )
    with pytest.raises(ValidationError):
        method.validate_input()


def test_invalid_x0():
    method = NumericalMethod(
        method="ode",
        input_data={
            "function": "x + y",
            "x0": "nope",
            "y0": 1,
            "x_end": 1,
            "h": 0.1,
            "calculation_mode": "euler",
        },
    )
    with pytest.raises(ValidationError):
        method.validate_input()


def test_invalid_h():
    method = NumericalMethod(
        method="ode",
        input_data={
            "function": "x + y",
            "x0": 0,
            "y0": 1,
            "x_end": 1,
            "h": -0.1,
            "calculation_mode": "euler",
        },
    )
    with pytest.raises(ValidationError):
        method.validate_input()


def test_system_requires_list_of_functions():
    method = NumericalMethod(
        method="ode",
        input_data={
            "system": "not a list",
            "y0": [1, 2],
            "x0": 0,
            "x_end": 1,
            "h": 0.1,
            "calculation_mode": "rk4_system",
        },
    )
    with pytest.raises(ValidationError):
        method.validate_input()


def test_shooting_requires_alpha_beta_s0():
    method = NumericalMethod(
        method="ode",
        input_data={
            "function": "x + y",
            "x0": 0,
            "x_end": 1,
            "h": 0.1,
            "calculation_mode": "shooting",
        },
    )
    with pytest.raises(ValidationError):
        method.validate_input()


def test_finite_differences_requires_n():
    method = NumericalMethod(
        method="ode",
        input_data={
            "function": "x",
            "x0": 0,
            "x_end": 1,
            "alpha": 0,
            "beta": 1,
            "calculation_mode": "finite_differences",
        },
    )
    with pytest.raises(ValidationError):
        method.validate_input()


# ============================================================
# EXECUTION TESTS
# ============================================================

def test_euler_simple():
    # y' = y, y(0)=1 → y = e^x
    method = NumericalMethod(
        method="ode",
        input_data={
            "function": "y",
            "x0": 0,
            "y0": 1,
            "x_end": 1,
            "h": 0.01,
            "calculation_mode": "euler",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    y_num = result["y"][-1]
    y_exact = np.e
    assert abs(y_num - y_exact) < 0.1


def test_heun_simple():
    method = NumericalMethod(
        method="ode",
        input_data={
            "function": "y",
            "x0": 0,
            "y0": 1,
            "x_end": 1,
            "h": 0.01,
            "calculation_mode": "heun",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    y_num = result["y"][-1]
    y_exact = np.e
    assert abs(y_num - y_exact) < 0.01


def test_rk2_simple():
    method = NumericalMethod(
        method="ode",
        input_data={
            "function": "y",
            "x0": 0,
            "y0": 1,
            "x_end": 1,
            "h": 0.01,
            "calculation_mode": "rk2",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    y_num = result["y"][-1]
    y_exact = np.e
    assert abs(y_num - y_exact) < 0.01


def test_rk4_simple():
    method = NumericalMethod(
        method="ode",
        input_data={
            "function": "y",
            "x0": 0,
            "y0": 1,
            "x_end": 1,
            "h": 0.01,
            "calculation_mode": "rk4",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    y_num = result["y"][-1]
    y_exact = np.e
    assert abs(y_num - y_exact) < 1e-4


def test_rk4_system():
    # System:
    # y1' = y1
    # y2' = -y2
    method = NumericalMethod(
        method="ode",
        input_data={
            "system": ["y", "-y"],
            "y0": [1, 1],
            "x0": 0,
            "x_end": 1,
            "h": 0.01,
            "calculation_mode": "rk4_system",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    y1_num = result["y"][-1][0]
    y2_num = result["y"][-1][1]

    assert abs(y1_num - np.e) < 1e-4
    assert abs(y2_num - np.exp(-1)) < 1e-4


def test_shooting_method():
    # y'' = 0 → y = ax + b
    # BVP: y(0)=0, y(1)=1 → y=x
    method = NumericalMethod(
        method="ode",
        input_data={
            "function": "0",   # y'' = 0
            "x0": 0,
            "x_end": 1,
            "alpha": 0,
            "beta": 1,
            "s0": 1,           # initial slope guess
            "h": 0.01,
            "calculation_mode": "shooting",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    assert abs(result["y_end"] - 1) < 0.05


def test_finite_differences():
    # y'' = 0, y(0)=0, y(1)=1 → y=x
    method = NumericalMethod(
        method="ode",
        input_data={
            "function": "0",
            "x0": 0,
            "x_end": 1,
            "alpha": 0,
            "beta": 1,
            "n": 10,
            "calculation_mode": "finite_differences",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    y = result["y"]
    x = result["x"]

    assert np.allclose(y, x, atol=0.05)


def test_adams_bashforth_2():
    method = NumericalMethod(
        method="ode",
        input_data={
            "function": "y",
            "x0": 0,
            "y0": 1,
            "x_end": 1,
            "h": 0.01,
            "calculation_mode": "adams_bashforth_2",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    y_num = result["y"][-1]
    assert abs(y_num - np.e) < 0.05


def test_adams_bashforth_3():
    method = NumericalMethod(
        method="ode",
        input_data={
            "function": "y",
            "x0": 0,
            "y0": 1,
            "x_end": 1,
            "h": 0.01,
            "calculation_mode": "adams_bashforth_3",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    y_num = result["y"][-1]
    assert abs(y_num - np.e) < 0.02


def test_adams_moulton_2():
    method = NumericalMethod(
        method="ode",
        input_data={
            "function": "y",
            "x0": 0,
            "y0": 1,
            "x_end": 1,
            "h": 0.01,
            "calculation_mode": "adams_moulton_2",
        },
    )

    method.validate_input()
    result = method.execute().get("result", {})

    y_num = result["y"][-1]
    assert abs(y_num - np.e) < 0.02
