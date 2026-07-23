import numpy as np
import pytest

from core.base_method import NumericalMethod
from core.exceptions import ConstructionError, ValidationError, ExecutionError

# ============================================================
# VALIDATION TESTS
# ============================================================

def test_missing_calculation_mode():
    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": [[1, 2], [3, 4]],
            "calculation_type": "matrix_operations"
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()


def test_missing_calculation_type():
    with pytest.raises(ConstructionError):
        NumericalMethod(
            method="linear_algebra",
            input_data={
                "A": [[1, 2], [3, 4]],
                "calculation_mode": "determinant"
            }
        )

def test_missing_matrix_A():
    with pytest.raises(ConstructionError):
        NumericalMethod(
            method="linear_algebra",
            input_data={
                "calculation_mode": "determinant",
                "calculation_type": "matrix_operations"
            }
    )

def test_matrix_A_not_2d():
    with pytest.raises(ConstructionError):
        NumericalMethod(
            method="linear_algebra",
            input_data={
                "A": [1, 2, 3],
                "calculation_mode": "determinant",
                "calculation_type": "matrix_operations"
        }
    )

def test_matrix_A_contains_nan():
    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": [[1, np.nan], [3, 4]],
            "calculation_mode": "determinant",
            "calculation_type": "matrix_operations"
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()


def test_system_solver_requires_b():
    with pytest.raises(ConstructionError):
        NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": [[1, 2], [3, 4]],
            "calculation_mode": "gauss",
            "calculation_type": "ec-system"
        }
    )



def test_dimension_mismatch_A_b():
    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": [[1, 2], [3, 4]],
            "b": [1, 2, 3],
            "calculation_mode": "gauss",
            "calculation_type": "ec-system"
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
            "calculation_mode": "cholesky",
            "calculation_type": "ec-system"
        }
    )

    with pytest.raises(ValidationError):
        method.validate_input()


def test_square_matrix_required():
    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": [[1, 2, 3], [4, 5, 6]],
            "calculation_mode": "determinant",
            "calculation_type": "matrix_operations"
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
            "calculation_mode": "determinant",
            "calculation_type": "matrix_operations"
        }
    )

    method.validate_input()
    result = method.execute()
    
    assert pytest.approx(result.get("result").get("value"), rel=1e-10) == -2.0


def test_inverse():
    A = [[4, 7], [2, 6]]

    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": A,
            "calculation_mode": "inverse",
            "calculation_type": "matrix_operations"
        }
    )

    method.validate_input()
    result = method.execute()

    expected = np.linalg.inv(np.array(A))
    assert np.allclose(result.get("result").get("value"), expected)


def test_gauss_solver():
    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": [[3, 2], [1, 2]],
            "b": [5, 5],
            "calculation_mode": "gauss",
            "calculation_type": "ec-system"
        }
    )

    method.validate_input()
    result = method.execute()

    assert np.allclose(result.get("result").get("solution"), [0, 2.5])


def test_gauss_jordan_solver():
    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": [[2, 1], [5, 7]],
            "b": [11, 13],
            "calculation_mode": "gauss_jordan",
            "calculation_type": "ec-system"
        }
    )

    method.validate_input()
    result = method.execute()

    assert np.allclose(result.get("result").get("solution"), [7.11111111, -3.22222222], atol=1e-6)


def test_cholesky_solver():
    A = [[4, 2], [2, 3]]
    b = [6, 7]

    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": A,
            "b": b,
            "calculation_mode": "cholesky",
            "calculation_type": "ec-system"
        }
    )

    method.validate_input()
    result = method.execute()

    expected = np.linalg.solve(np.array(A), np.array(b))
    assert np.allclose(result.get("result").get("solution"), expected)


def test_qr_solver():
    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": [[1, 1], [1, -1]],
            "b": [2, 0],
            "calculation_mode": "qr",
            "calculation_type": "ec-system"
        }
    )

    method.validate_input()
    result = method.execute()

    assert np.allclose(result.get("result").get("solution"), [1, 1])


def test_jacobi_solver():
    A = [[4, 1], [2, 3]]
    b = [1, 2]

    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": A,
            "b": b,
            "calculation_mode": "jacobi",
            "calculation_type": "ec-system"
        }
    )

    method.validate_input()
    result = method.execute()

    expected = np.linalg.solve(np.array(A), np.array(b))
    assert np.allclose(result.get("result").get("solution"), expected, atol=1e-6)


def test_gauss_seidel_solver():
    A = [[4, 1], [2, 3]]
    b = [1, 2]

    method = NumericalMethod(
        method="linear_algebra",
        input_data={
            "A": A,
            "b": b,
            "calculation_mode": "gauss_seidel",
            "calculation_type": "ec-system"
        }
    )

    method.validate_input()
    result = method.execute()

    expected = np.linalg.solve(np.array(A), np.array(b))
    assert np.allclose(result.get("result").get("solution"), expected, atol=1e-6)


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
            "calculation_mode": "lu",
            "calculation_type": "ec-system"
        }
    )

    method.validate_input()
    result = method.execute()

    P = result.get("result").get("P")
    L = result.get("result").get("L")
    U = result.get("result").get("U")

    PA = P @ A
    LU = L @ U

    assert np.allclose(PA, LU)
