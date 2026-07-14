import numpy as np
import re
from core.exceptions import ConstructionError


class NumericalDerivative:
    """
    Constructor for numerical derivatives.
    This class ONLY stores input_data and exposes attributes
    used by the validator and executor.
    """

    def __init__(self, input_data):
        self.input_data = input_data

        # ───────────────────────────────────────────────
        # Required fields
        # ───────────────────────────────────────────────
        self.function = input_data.get("function")
        self.calculation_mode = input_data.get("calculation_mode")

        # ───────────────────────────────────────────────
        # Validate function exists
        # ───────────────────────────────────────────────
        if not self.function or not isinstance(self.function, str):
            raise ConstructionError("A valid function string is required.")

        # ───────────────────────────────────────────────
        # Validate x (always required)
        # ───────────────────────────────────────────────
        try:
            self.x = float(input_data.get("x"))
        except Exception:
            raise ConstructionError("x must be a valid float.")

        # ───────────────────────────────────────────────
        # Validate h (always required)
        # ───────────────────────────────────────────────
        try:
            self.h = float(input_data.get("h"))
        except Exception:
            raise ConstructionError("h must be a valid float.")

        # ───────────────────────────────────────────────
        # Validate y only for partial derivatives
        # ───────────────────────────────────────────────
        if self.calculation_mode == "partial_y":
            try:
                self.y = float(input_data.get("y"))
            except Exception:
                raise ConstructionError("y must be a valid float for partial derivatives.")
        elif self.calculation_mode == "partial_x":
            try:
                self.x = float(input_data.get("x"))
            except Exception:
                raise ConstructionError("x must be a valid float for partial derivatives.")    
        else:
            self.y = None

        # ───────────────────────────────────────────────
        # Validate Richardson order (optional)
        # ───────────────────────────────────────────────
        if "richardson_order" in input_data:
            try:
                self.richardson_order = int(input_data.get("richardson_order"))
                if self.richardson_order < 1:
                    raise ConstructionError("Richardson order must be >= 1.")
            except Exception:
                raise ConstructionError("Richardson order must be an integer >= 1.")
        else:
            self.richardson_order = 2  # default

        # ───────────────────────────────────────────────
        # Validate function variables
        # ───────────────────────────────────────────────
        self._validate_function_variables()

    # ============================================================
    # Helper: validate allowed variables in function
    # ============================================================
    def _validate_function_variables(self):
        """
        Ensures the function only contains allowed variables:
        - Normal derivative: only x
        - Partial derivative: x and y
        """

        # Extract variable names (alphabetic tokens)
        tokens = re.findall(r"[a-zA-Z]+", self.function)

        allowed = {"x"} if self.calculation_mode not in ["partial_x", "partial_y"] else {"x", "y"}

        for t in tokens:
            if t not in allowed:
                raise ConstructionError(
                    f"Invalid variable '{t}' in function. "
                    f"Allowed variables: {allowed}."
                )
