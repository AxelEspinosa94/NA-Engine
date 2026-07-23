# scripts/smoke_linear_algebra.py
import sys
import os

# Ensure project root is in the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from core.base_method import NumericalMethod
from core.contract import UIContract

contract = UIContract()

"""
Smoke test for Linear Algebra module.

We test:
- Determinant (matrix operation)
- Gauss (system solver)
- LU decomposition
- QR decomposition
- Cholesky decomposition

Goal:
Confirm the entire pipeline works:
Constructor → Validator → Executor → Renderer → UIContract
"""

# ============================================================
# 1. MATRIX OPERATION: determinant
# ============================================================

input_det = {
    "A": [[1, 2], [3, 4]],
    "calculation_mode": "determinant",
    "calculation_type": "matrix_operations"
}

nm_det = NumericalMethod("linear_algebra", input_det)
nm_det.validate_input()
outcome_det = nm_det.execute()

print("\n=== DETERMINANT OUTCOME ===")
print(outcome_det)

payload_det = contract.resolve("determinant", outcome_det)
print("\n=== DETERMINANT PAYLOAD TYPE ===")
print(payload_det.children[0].children if payload_det.children else "empty")


# ============================================================
# 2. SYSTEM SOLVER: Gauss
# ============================================================

input_gauss = {
    "A": [[3, 2], [1, 2]],
    "b": [5, 5],
    "calculation_mode": "gauss",
    "calculation_type": "ec-system"
}

nm_gauss = NumericalMethod("linear_algebra", input_gauss)
nm_gauss.validate_input()
outcome_gauss = nm_gauss.execute()

print("\n=== GAUSS OUTCOME ===")
print(outcome_gauss)

payload_gauss = contract.resolve("gauss", outcome_gauss)
print("\n=== GAUSS PAYLOAD TYPE ===")
print(payload_gauss.children[0].children if payload_gauss.children else "empty")


# ============================================================
# 3. LU DECOMPOSITION
# ============================================================

input_lu = {
    "A": [[2, 1, 1],
          [4, -6, 0],
          [-2, 7, 2]],
    "b": [5, -2, 9],
    "calculation_mode": "lu",
    "calculation_type": "ec-system"
}

nm_lu = NumericalMethod("linear_algebra", input_lu)
nm_lu.validate_input()
outcome_lu = nm_lu.execute()

print("\n=== LU OUTCOME ===")
print(outcome_lu)

payload_lu = contract.resolve("lu", outcome_lu)
print("\n=== LU PAYLOAD TYPE ===")
print(payload_lu.children[0].children if payload_lu.children else "empty")


# ============================================================
# 4. QR DECOMPOSITION
# ============================================================

input_qr = {
    "A": [[1, 1], [1, -1]],
    "b": [2, 0],
    "calculation_mode": "qr",
    "calculation_type": "ec-system"
}

nm_qr = NumericalMethod("linear_algebra", input_qr)
nm_qr.validate_input()
outcome_qr = nm_qr.execute()

print("\n=== QR OUTCOME ===")
print(outcome_qr)

payload_qr = contract.resolve("qr", outcome_qr)
print("\n=== QR PAYLOAD TYPE ===")
print(payload_qr.children[0].children if payload_qr.children else "empty")


# ============================================================
# 5. CHOLESKY DECOMPOSITION
# ============================================================

input_chol = {
    "A": [[4, 2], [2, 3]],
    "b": [6, 7],
    "calculation_mode": "cholesky",
    "calculation_type": "ec-system"
}

nm_chol = NumericalMethod("linear_algebra", input_chol)
nm_chol.validate_input()
outcome_chol = nm_chol.execute()

print("\n=== CHOLESKY OUTCOME ===")
print(outcome_chol)

payload_chol = contract.resolve("cholesky", outcome_chol)
print("\n=== CHOLESKY PAYLOAD TYPE ===")
print(payload_chol.children[0].children if payload_chol.children else "empty")
