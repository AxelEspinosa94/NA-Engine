import numpy as np
from core.exceptions import ConstructionError

class ODE:
    """
    Constructor for Ordinary Differential Equations (ODEs).
    Performs structural validation and stores parsed fields.
    Mathematical validation is done in the validator layer.
    """

    VALID_MODES = {
        "euler",
        "heun",
        "rk2",
        "rk4",
        "rk4_system",
        "shooting",
        "finite_differences",
        "adams_bashforth_2",
        "adams_bashforth_3",
        "adams_moulton_2",
    }

    def __init__(self, input_data):
        if not isinstance(input_data, dict):
            raise ConstructionError("input_data must be a dictionary.")
        
        self.input_data = input_data

        # ------------------------------------------------------------
        # 1. Validate calculation_mode
        # ------------------------------------------------------------
        mode = input_data.get("calculation_mode")
        if mode is None:
            raise ConstructionError("Missing 'calculation_mode'.")
        if mode not in self.VALID_MODES:
            raise ConstructionError(f"Invalid calculation_mode: {mode}")

        self.calculation_mode = mode

        # ------------------------------------------------------------
        # 2. Common fields (IVP)
        # ------------------------------------------------------------
        self.f = input_data.get("function")
        self.x0 = input_data.get("x0")
        self.y0 = input_data.get("y0")
        self.x_end = input_data.get("x_end")
        self.h = input_data.get("h")

        # ------------------------------------------------------------
        # 3. System fields
        # ------------------------------------------------------------
        self.system = input_data.get("system")

        # ------------------------------------------------------------
        # 4. BVP fields (shooting / finite differences)
        # ------------------------------------------------------------
        self.alpha = input_data.get("alpha")
        self.beta = input_data.get("beta")
        self.s0 = input_data.get("s0")
        self.n = input_data.get("n")

        # ------------------------------------------------------------
        # 5. Structural validation per mode
        # ------------------------------------------------------------
        if mode in {"euler", "heun", "rk2", "rk4", "adams_bashforth_2", "adams_bashforth_3", "adams_moulton_2"}:
            self._validate_ivp()

        elif mode == "rk4_system":
            self._validate_system()

        elif mode == "shooting":
            self._validate_shooting()

        elif mode == "finite_differences":
            self._validate_finite_diff()

    # ======================================================================
    # VALIDATION HELPERS
    # ======================================================================

    def _validate_ivp(self):
        """IVP methods require f(x,y), x0, y0, x_end, h."""
        if not isinstance(self.f, str):
            raise ConstructionError("IVP requires 'function' as a string.")

        for field, name in [(self.x0, "x0"), (self.y0, "y0"), (self.x_end, "x_end"), (self.h, "h")]:
            if field is None:
                raise ConstructionError(f"Missing '{name}' for IVP.")
            try:
                float(field)
            except Exception:
                raise ConstructionError(f"'{name}' must be numeric.")

    def _validate_system(self):
        """System ODEs require list of functions and vector y0."""
        if not isinstance(self.system, list) or len(self.system) == 0:
            raise ConstructionError("'system' must be a non-empty list of functions.")

        if not all(isinstance(expr, str) for expr in self.system):
            raise ConstructionError("'system' must contain function strings.")

        if not isinstance(self.y0, list):
            raise ConstructionError("'y0' must be a list for system ODEs.")

        if len(self.y0) != len(self.system):
            raise ConstructionError("Length of 'y0' must match number of system equations.")

        for field, name in [(self.x0, "x0"), (self.x_end, "x_end"), (self.h, "h")]:
            if field is None:
                raise ConstructionError(f"Missing '{name}' for system ODE.")
            try:
                float(field)
            except Exception:
                raise ConstructionError(f"'{name}' must be numeric.")

    def _validate_shooting(self):
        """Shooting requires f(x,y), x0, x_end, alpha, beta, s0, h."""
        required = {
            "function": self.f,
            "x0": self.x0,
            "x_end": self.x_end,
            "alpha": self.alpha,
            "beta": self.beta,
            "s0": self.s0,
            "h": self.h,
        }

        for name, value in required.items():
            if value is None:
                raise ConstructionError(f"Shooting method requires '{name}'.")
            if name != "function":
                try:
                    float(value)
                except Exception:
                    raise ConstructionError(f"'{name}' must be numeric.")

        if not isinstance(self.f, str):
            raise ConstructionError("'function' must be a string.")

    def _validate_finite_diff(self):
        """Finite differences require f(x,y), x0, x_end, alpha, beta, n."""
        required = {
            "function": self.f,
            "x0": self.x0,
            "x_end": self.x_end,
            "alpha": self.alpha,
            "beta": self.beta,
            "n": self.n,
        }

        for name, value in required.items():
            if value is None:
                raise ConstructionError(f"Finite differences require '{name}'.")
            if name != "function":
                try:
                    float(value)
                except Exception:
                    raise ConstructionError(f"'{name}' must be numeric.")

        if not isinstance(self.f, str):
            raise ConstructionError("'function' must be a string.")

        if int(self.n) <= 1:
            raise ConstructionError("'n' must be an integer greater than 1.")
