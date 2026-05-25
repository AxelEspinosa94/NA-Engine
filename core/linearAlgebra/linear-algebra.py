import numpy as np
from core.exceptions import ValidationError

class LinearAlgebra:
    """
    Constructor for matrix operations and linear system solvers.
    This class ONLY prepares input data and exposes attributes
    used by the validator and executor.
    """

    def __init__(self, input_data):
        self.input_data = input_data

        # Required for all operations
        self.A = None
        if "A" in input_data:
            self.A = np.array(input_data["A"], dtype=float)

        # Optional: only required for system solvers
        self.b = None
        if "b" in input_data:
            self.b = np.array(input_data["b"], dtype=float)

        # Required for dispatching
        self.calculation_mode = input_data.get("calculation_mode")
