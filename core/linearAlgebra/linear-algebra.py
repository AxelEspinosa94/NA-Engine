import numpy as np
from core.exceptions import ConstructionError

class LinearAlgebra:
    """
    Constructor for matrix operations and linear system solvers.
    """

    def __init__(self, input_data):
        self.input_data = input_data
        self.calculation_type = input_data.get("calculation_type")
        # "calculation_type" can be either "matrix_operations" or "ec-system"
        if self.calculation_type not in ("matrix_operations", "ec-system"):
            raise ConstructionError("Invalid calculation_type for Linear Algebra module.")

        # Required for all operations
        if "A" not in input_data:
            raise ConstructionError("Matrix A is required for linear algebra operations.")

        self.A = np.array(input_data["A"], dtype=float)

        if self.A.ndim != 2:
            raise ConstructionError("Matrix A must be 2-dimensional.")

        # Optional: only required for system solvers
        self.b = None
        if self.calculation_type == "ec-system" and "b" not in input_data:
            raise ConstructionError("Vector b is required for linear system solvers.")
        elif self.calculation_type == "ec-system" and "b" in input_data:
            self.b = np.array(input_data["b"], dtype=float)
            if self.b.ndim != 1:
                raise ConstructionError("Vector b must be 1-dimensional.")

        # Required for dispatching
        self.calculation_mode = input_data.get("calculation_mode")
