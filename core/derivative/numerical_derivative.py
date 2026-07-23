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
        self._normalize_function()
        self._validate_function_variables()
        

    # ============================================================
    # Helper: validate allowed variables in function
    # ============================================================
    def _validate_function_variables(self):
        tokens = re.findall(r"[a-zA-Z_]+", self.function)

        allowed_vars = {"x"} if self.calculation_mode not in ["partial_x", "partial_y"] else {"x", "y"}

        allowed_funcs = {
            "np", "sin", "cos", "tan", "exp", "log", "sqrt"
        }

        for t in tokens:
            if t in allowed_funcs:
                continue
            if t == "np":
                continue
            if t not in allowed_vars:
                raise ConstructionError(
                    f"Invalid variable '{t}' in function. Allowed variables: {allowed_vars}."
                )


    def _normalize_function(self):
        """
        Converts common math functions to numpy equivalents.
        Example: sin(x) -> np.sin(x)
        """
        replacements = {
            "sin": "np.sin",
            "cos": "np.cos",
            "tan": "np.tan",
            "exp": "np.exp",
            "log": "np.log",
            "sqrt": "np.sqrt",
        }

        expr = self.function

        for k, v in replacements.items():
            expr = re.sub(rf"\b{k}\b", v, expr)

        self.function = expr
