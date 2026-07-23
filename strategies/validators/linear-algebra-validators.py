import numpy as np
from typing import Dict, Any
from core.exceptions import ValidationError


class LinearAlgebraValidator:

    SYSTEM_MODES = [
        "gauss", "gauss_jordan", "lu", "cholesky", "qr",
        "jacobi", "gauss_seidel"
    ]

    MATRIX_MODES = [
        "determinant", "inverse", "norm",
        "condition_number", "transpose", "rank"
    ]

    def validate(self, input_data: Dict[str, Any]):

        # ---------------------------
        # Validate calculation_type
        # ---------------------------
        calc_type = input_data.get("calculation_type")
        if calc_type not in ("matrix_operations", "ec-system"):
            raise ValidationError(
                "calculation_type must be either 'matrix_operations' or 'ec-system'."
            )

        # ---------------------------
        # Validate calculation_mode
        # ---------------------------
        mode = input_data.get("calculation_mode")
        if mode is None:
            raise ValidationError("calculation_mode is required for LinearAlgebra.")

        if calc_type == "matrix_operations" and mode not in self.MATRIX_MODES:
            raise ValidationError(f"{mode} is not a valid matrix operation.")

        if calc_type == "ec-system" and mode not in self.SYSTEM_MODES:
            raise ValidationError(f"{mode} is not a valid system solver.")

        # ---------------------------
        # Validate A
        # ---------------------------
        A = input_data.get("A")
        if A is None:
            raise ValidationError("Matrix A is required.")

        A = np.array(A, dtype=float)

        if A.ndim != 2:
            raise ValidationError("Matrix A must be 2-dimensional.")

        if np.isnan(A).any() or np.isinf(A).any():
            raise ValidationError("Matrix A contains NaN or infinity.")

        # ---------------------------
        # Validate b only for system solvers
        # ---------------------------
        if calc_type == "ec-system":

            b = input_data.get("b")
            if b is None:
                raise ValidationError("Vector b is required for solving linear systems.")

            b = np.array(b, dtype=float)

            if b.ndim != 1:
                raise ValidationError("Vector b must be 1-dimensional.")

            if A.shape[0] != b.shape[0]:
                raise ValidationError("Dimensions of A and b do not match.")

        # ---------------------------
        # Square matrix required (only for specific modes)
        # ---------------------------
        if mode in ["determinant", "inverse", "lu", "cholesky", "qr"]:
            if A.shape[0] != A.shape[1]:
                raise ValidationError(f"{mode} requires a square matrix.")

        # ---------------------------
        # Cholesky-specific validation
        # ---------------------------
        if mode == "cholesky":
            if not np.allclose(A, A.T):
                raise ValidationError("Cholesky requires a symmetric matrix.")

        return True
