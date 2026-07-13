from core.exceptions import ValidationError, ConstructionError, ExecutionError
import numpy as np
import pytest
import io
import base64

from core.base_method import NumericalMethod
from core.contract import UIContract

contract = UIContract()

# Mark entire module as pending until Stage 4 is complete
pytestmark = pytest.mark.pending


# ═══════════════════════════════════════════════════════════════
# 1. VOLUME TESTS — large matrices (50–500+)
# ═══════════════════════════════════════════════════════════════

@pytest.mark.parametrize("n", [50, 100, 200])
def test_large_matrix_determinant(n):
    A = np.random.rand(n, n).tolist()

    nm = NumericalMethod("linear_algebra", {
        "A": A,
        "calculation_mode": "determinant",
        "calculation_type": "matrix_operations",
    })

    nm.validate_input()
    result = nm.execute()
    result = result.get("result")

    assert "value" in result
    assert isinstance(result["value"], float)


@pytest.mark.parametrize("n", [50, 100])
def test_large_system_gauss(n):
    A = np.random.rand(n, n)
    b = np.random.rand(n)

    nm = NumericalMethod("linear_algebra", {
        "A": A.tolist(),
        "b": b.tolist(),
        "calculation_mode": "gauss",
        "calculation_type": "ec-system",
    })

    nm.validate_input()
    result = nm.execute()
    result = result.get("result")

    assert "solution" in result
    assert len(result["solution"]) == n


# ═══════════════════════════════════════════════════════════════
# 2. PRECISION TESTS — compare against analytical ground truth
# ═══════════════════════════════════════════════════════════════

def test_precision_inverse():
    A = np.array([[4, 7], [2, 6]])
    expected = np.linalg.inv(A)

    nm = NumericalMethod("linear_algebra", {
        "A": A.tolist(),
        "calculation_mode": "inverse",
        "calculation_type": "matrix_operations",
    })

    nm.validate_input()
    result = nm.execute()
    result = result.get("result")

    assert np.allclose(result["value"], expected, atol=1e-12)


def test_precision_qr():
    A = np.array([[1, 1], [1, -1]])
    b = np.array([2, 0])
    expected = np.linalg.solve(A, b)

    nm = NumericalMethod("linear_algebra", {
        "A": A.tolist(),
        "b": b.tolist(),
        "calculation_mode": "qr",
        "calculation_type": "ec-system",
    })

    nm.validate_input()
    result = nm.execute()
    result = result.get("result")

    assert np.allclose(result["solution"], expected, atol=1e-12)


# ═══════════════════════════════════════════════════════════════
# 3. STABILITY TESTS — determinism (same input → same output)
# ═══════════════════════════════════════════════════════════════

def test_stability_gauss():
    A = [[3, 2], [1, 2]]
    b = [5, 5]

    nm1 = NumericalMethod("linear_algebra", {
        "A": A,
        "b": b,
        "calculation_mode": "gauss",
        "calculation_type": "ec-system",
    })

    nm2 = NumericalMethod("linear_algebra", {
        "A": A,
        "b": b,
        "calculation_mode": "gauss",
        "calculation_type": "ec-system",
    })

    nm1.validate_input()
    nm2.validate_input()

    r1 = nm1.execute()
    r2 = nm2.execute()

    r1 = r1.get("result")
    r2 = r2.get("result")

    assert np.allclose(r1["solution"], r2["solution"])


# ═══════════════════════════════════════════════════════════════
# 4. ERROR HANDLING — invalid formats
# ═══════════════════════════════════════════════════════════════

def test_error_invalid_matrix_shape():

    with pytest.raises(ConstructionError):
        NumericalMethod("linear_algebra", {
            "A": [[1, 2, 3], [4, 5]],  # ragged matrix
            "calculation_mode": "determinant",
            "calculation_type": "matrix_operations",
        })


def test_error_missing_b_for_system():
    with pytest.raises(ConstructionError):
        NumericalMethod("linear_algebra", {
            "A": [[1, 2], [3, 4]],
            "calculation_mode": "gauss",
            "calculation_type": "ec-system",
        })

# ═══════════════════════════════════════════════════════════════
# 5. UPLOAD TESTS — CSV / TXT / Excel
# ═══════════════════════════════════════════════════════════════

def encode_upload(text: str):
    """Utility to simulate Dash upload contents."""
    return "data:text/plain;base64," + base64.b64encode(text.encode()).decode()


def test_upload_txt_matrix():
    txt = "1 2 3\n4 5 6\n7 8 9"
    contents = encode_upload(txt)

    nm = NumericalMethod("linear_algebra", {
        "A": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        "calculation_mode": "rank",
        "calculation_type": "matrix_operations",
    })

    nm.validate_input()
    result = nm.execute()
    result = result.get("result")

    assert "value" in result


def test_upload_txt_system():
    txt = "3x + 2y = 5\nx - y = 1"
    contents = encode_upload(txt)

    # Expected matrix
    A = [[3, 2], [1, -1]]
    b = [5, 1]

    nm = NumericalMethod("linear_algebra", {
        "A": A,
        "b": b,
        "calculation_mode": "gauss",
        "calculation_type": "ec-system",
    })

    nm.validate_input()
    result = nm.execute()
    result = result.get("result")

    assert "solution" in result


# ═══════════════════════════════════════════════════════════════
# 6. FULL PIPELINE — upload/table → NumericalMethod → UIContract
# ═══════════════════════════════════════════════════════════════

def test_full_pipeline_matrix():
    A = [[1, 2], [3, 4]]

    nm = NumericalMethod("linear_algebra", {
        "A": A,
        "calculation_mode": "determinant",
        "calculation_type": "matrix_operations",
    })

    nm.validate_input()
    outcome = nm.execute()

    payload = contract.resolve("determinant", outcome)

    assert payload is not None
    assert hasattr(payload, "children")


def test_full_pipeline_system():
    A = [[3, 2], [1, 2]]
    b = [5, 5]

    nm = NumericalMethod("linear_algebra", {
        "A": A,
        "b": b,
        "calculation_mode": "gauss",
        "calculation_type": "ec-system",
    })

    nm.validate_input()
    outcome = nm.execute()

    payload = contract.resolve("gauss", outcome)

    assert payload is not None
    assert hasattr(payload, "children")
