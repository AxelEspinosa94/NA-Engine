import numpy as np
import pytest

from core.base_method import NumericalMethod
from core.exceptions import ValidationError, ExecutionError


# ============================================================
# VALIDATION TESTS
# ============================================================

def test_missing_calculation_mode():
    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": [[1, 2], [3, 4]]
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()


def test_missing_matrix_A():
    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "calculation_mode": "determinant"
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()


def test_matrix_A_not_2d():
    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": [1, 2, 3],
            "calculation_mode": "determinant"
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()


def test_matrix_A_contains_nan():
    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": [[1, np.nan], [3, 4]],
            "calculation_mode": "determinant"
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()


def test_system_solver_requires_b():
    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": [[1, 2], [3, 4]],
            "calculation_mode": "gauss"
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()


def test_dimension_mismatch_A_b():
    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": [[1, 2], [3, 4]],
            "b": [1, 2, 3],
            "calculation_mode": "gauss"
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()


def test_cholesky_requires_symmetric_matrix():
    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": [[1, 2], [3, 4]],
            "b": [1, 1],
            "calculation_mode": "cholesky"
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()


def test_square_matrix_required():
    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": [[1, 2, 3], [4, 5, 6]],
            "calculation_mode": "determinant"
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()


# ============================================================
# EXECUTION TESTS
# ============================================================

def test_determinant():
    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": [[1, 2], [3, 4]],
            "calculation_mode": "determinant"
        }
    )

    method.validate_input()
    result = method.execute().get("result", {})

    assert pytest.approx(result["determinant"], rel=1e-10) == -2.0


def test_inverse():
    A = [[4, 7], [2, 6]]

    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": A,
            "calculation_mode": "inverse"
        }
    )

    method.validate_input()
    result = method.execute().get("result", {})

    expected = np.linalg.inv(np.array(A))
    assert np.allclose(result["inverse"], expected)


def test_gauss_solver():
    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": [[3, 2], [1, 2]],
            "b": [5, 5],
            "calculation_mode": "gauss"
        }
    )

    method.validate_input()
    result = method.execute().get("result", {})

    assert np.allclose(result["solution"], [0, 2.5])


def test_gauss_jordan_solver():
    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": [[2, 1], [5, 7]],
            "b": [11, 13],
            "calculation_mode": "gauss_jordan"
        }
    )

    method.validate_input()
    result = method.execute().get("result", {})

    assert np.allclose(result["solution"], [7.11111111, -3.22222222], atol=1e-6)


def test_cholesky_solver():
    A = [[4, 2], [2, 3]]
    b = [6, 7]

    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": A,
            "b": b,
            "calculation_mode": "cholesky"
        }
    )

    method.validate_input()
    result = method.execute().get("result", {})

    expected = np.linalg.solve(np.array(A), np.array(b))
    assert np.allclose(result["solution"], expected)


def test_qr_solver():
    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": [[1, 1], [1, -1]],
            "b": [2, 0],
            "calculation_mode": "qr"
        }
    )

    method.validate_input()
    result = method.execute().get("result", {})

    assert np.allclose(result["solution"], [1, 1])


def test_jacobi_solver():
    A = [[4, 1], [2, 3]]
    b = [1, 2]

    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": A,
            "b": b,
            "calculation_mode": "jacobi"
        }
    )

    method.validate_input()
    result = method.execute().get("result", {})

    expected = np.linalg.solve(np.array(A), np.array(b))
    assert np.allclose(result["solution"], expected, atol=1e-6)


def test_gauss_seidel_solver():
    A = [[4, 1], [2, 3]]
    b = [1, 2]

    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": A,
            "b": b,
            "calculation_mode": "gauss_seidel"
        }
    )

    method.validate_input()
    result = method.execute().get("result", {})

    expected = np.linalg.solve(np.array(A), np.array(b))
    assert np.allclose(result["solution"], expected, atol=1e-6)


# ============================================================
# LU DECOMPOSITION (WITH PARTIAL PIVOTING)
# ============================================================

def test_lu_decomposition_partial_pivoting():
    A = np.array([[2, 1, 1],
                  [4, -6, 0],
                  [-2, 7, 2]], dtype=float)

    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": A.tolist(),
            "b": [5, -2, 9],
            "calculation_mode": "lu"
        }
    )

    method.validate_input()
    result = method.execute().get("result", {})

    P = result["P"]
    L = result["L"]
    U = result["U"]

    # Check PA = LU
    PA = P @ A
    LU = L @ U

    assert np.allclose(PA, LU)
