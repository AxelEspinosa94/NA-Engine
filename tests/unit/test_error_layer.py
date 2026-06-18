import pytest
from core.error_normalizer import ErrorNormalizer
from core.exceptions import ConstructionError, ValidationError, ExecutionError
from core.base_method import NumericalMethod


# ---------------------------------------------------------
# 1. Unit tests for ErrorNormalizer.normalize()
# ---------------------------------------------------------

def test_normalize_validation_error():
    exc = ValidationError("invalid input")
    result = ErrorNormalizer.normalize(exc, "ode", {"x0": "abc"})

    assert result["status"] == "error"
    assert result["error_type"] == "ValidationError"
    assert result["message"] == "invalid input"
    assert result["context"]["method"] == "ode"


def test_normalize_execution_error():
    exc = ExecutionError("division by zero")
    result = ErrorNormalizer.normalize(exc, "nonlinear", {})

    assert result["error_type"] == "ExecutionError"
    assert "division by zero" in result["message"]


def test_normalize_math_error():
    exc = ZeroDivisionError("float division by zero")
    result = ErrorNormalizer.normalize(exc, "integration", {})

    assert result["error_type"] == "MathError"


def test_normalize_syntax_error():
    exc = SyntaxError("invalid syntax")
    result = ErrorNormalizer.normalize(exc, "ode", {})

    assert result["error_type"] == "FunctionSyntaxError"


def test_normalize_name_error():
    exc = NameError("name 'xp' is not defined")
    result = ErrorNormalizer.normalize(exc, "ode", {})

    assert result["error_type"] == "FunctionNameError"


def test_normalize_internal_error():
    exc = RuntimeError("unexpected failure")
    result = ErrorNormalizer.normalize(exc, "ode", {})

    assert result["error_type"] == "InternalError"


# ---------------------------------------------------------
# 2. Integration tests with NumericalMethod.execute()
# ---------------------------------------------------------

def test_execute_returns_normalized_validation_error():
    with pytest.raises(ValidationError):
        NumericalMethod(
            method="nonlinear",
            input_data={
                "mode": "function",
                "function": "x**2",
                "interval": "not-an-interval",  # invalid
                "calculation_mode": "bisection",
            },
        ).validate_input()


def test_execute_returns_normalized_execution_error():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "1/x",  # division by zero at x=0
            "interval": [-1, 1],
            "calculation_mode": "bisection",
        },
    )
    method.validate_input()
    response = method.execute()

    assert response["status"] == "error"
    assert response["error_type"] == "ExecutionError" or response["error_type"] == "MathError"


def test_execute_success_format():
    method = NumericalMethod(
        method="nonlinear",
        input_data={
            "mode": "function",
            "function": "x",
            "interval": [-1, 1],
            "calculation_mode": "bisection",
        },
    )
    method.validate_input()
    response = method.execute()

    assert "status" in response
    assert response["status"] in ("success", "error")
    # If success, must contain result
    if response["status"] == "success":
        assert "result" in response


# ---------------------------------------------------------
# 3. Format validation
# ---------------------------------------------------------

def test_error_format_contains_required_fields():
    exc = ValidationError("bad input")
    result = ErrorNormalizer.normalize(exc, "ode", {"x0": 10})

    assert set(result.keys()) == {"status", "error_type", "message", "context"}
    assert "method" in result["context"]
    assert "input_data" in result["context"]



def test_normalize_construction_error():
    exc = ConstructionError("invalid constructor state")
    result = ErrorNormalizer.normalize(exc, "interpolation", {"points": None})

    assert result["status"] == "error"
    assert result["error_type"] == "ConstructionError"
    assert result["message"] == "invalid constructor state"
    assert result["context"]["method"] == "interpolation"


def test_execute_returns_normalized_construction_error():
    # Provoca un ConstructionError al construir el método
    
    with pytest.raises(ConstructionError):
        NumericalMethod(
            method="lagrange",
            input_data={
                "mode": "lagrange",
                "points": "corrupted",  # fuerza ConstructionError
            },
        )

def test_construction_error_is_not_validation_error():
    exc = ConstructionError("bad structure")
    result = ErrorNormalizer.normalize(exc, "ode", {})

    assert result["error_type"] != "ValidationError"
