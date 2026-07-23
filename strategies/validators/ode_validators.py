import numbers
from core.exceptions import ValidationError


class ODEValidator:
    """
    Strict validation for ODE solvers.
    Accepts input_data directly.
    """

    SUPPORTED_MODES = [
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
    ]

    def validate(self, input_data):

        mode = input_data.get("calculation_mode")
        if mode not in self.SUPPORTED_MODES:
            raise ValidationError(f"Unsupported calculation_mode: {mode}")

        # ============================================================
        # 1. IVP METHODS (single ODE)
        # ============================================================
        if mode in [
            "euler",
            "heun",
            "rk2",
            "rk4",
            "adams_bashforth_2",
            "adams_bashforth_3",
            "adams_moulton_2",
        ]:

            # function
            f = input_data.get("function")
            if not isinstance(f, str) or f.strip() == "":
                raise ValidationError("function must be a non-empty string.")

            # x0, y0, x_end
            for key in ["x0", "y0", "x_end"]:
                val = input_data.get(key)
                if not isinstance(val, numbers.Real):
                    raise ValidationError(f"{key} must be a real number.")

            # h
            h = input_data.get("h")
            if not isinstance(h, numbers.Real) or h <= 0:
                raise ValidationError("h must be a positive real number.")

            # domain check
            if input_data["x_end"] <= input_data["x0"]:
                raise ValidationError("x_end must be greater than x0.")

        # ============================================================
        # 2. SYSTEM OF ODEs (RK4 system)
        # ============================================================
        if mode == "rk4_system":
            system = input_data.get("system")
            y0 = input_data.get("y0")

            if not isinstance(system, list) or len(system) == 0:
                raise ValidationError("system must be a non-empty list of functions.")

            if not all(isinstance(f, str) for f in system):
                raise ValidationError("system must contain function strings.")

            if not isinstance(y0, list):
                raise ValidationError("y0 must be a list for system ODEs.")

            if len(y0) != len(system):
                raise ValidationError("Length of y0 must match number of system equations.")

            # numeric fields
            for key in ["x0", "x_end", "h"]:
                val = input_data.get(key)
                if not isinstance(val, numbers.Real):
                    raise ValidationError(f"{key} must be a real number.")

            if input_data["h"] <= 0:
                raise ValidationError("h must be positive.")

            if input_data["x_end"] <= input_data["x0"]:
                raise ValidationError("x_end must be greater than x0.")

        # ============================================================
        # 3. SHOOTING METHOD (BVP)
        # ============================================================
        if mode == "shooting":
            required = ["function", "x0", "x_end", "alpha", "beta", "s0", "h"]

            for key in required:
                if key not in input_data:
                    raise ValidationError(f"{key} is required for shooting method.")

            if not isinstance(input_data["function"], str):
                raise ValidationError("function must be a string.")

            # numeric fields
            for key in ["x0", "x_end", "alpha", "beta", "s0", "h"]:
                val = input_data.get(key)
                if not isinstance(val, numbers.Real):
                    raise ValidationError(f"{key} must be a real number.")

            if input_data["h"] <= 0:
                raise ValidationError("h must be positive.")

            if input_data["x_end"] <= input_data["x0"]:
                raise ValidationError("x_end must be greater than x0.")

        # ============================================================
        # 4. FINITE DIFFERENCES (BVP)
        # ============================================================
        if mode == "finite_differences":
            required = ["function", "x0", "x_end", "alpha", "beta", "n"]

            for key in required:
                if key not in input_data:
                    raise ValidationError(f"{key} is required for finite differences.")

            if not isinstance(input_data["function"], str):
                raise ValidationError("function must be a string.")

            # numeric fields
            for key in ["x0", "x_end", "alpha", "beta"]:
                val = input_data.get(key)
                if not isinstance(val, numbers.Real):
                    raise ValidationError(f"{key} must be a real number.")

            # n
            n = input_data.get("n")
            if not isinstance(n, int) or n < 3:
                raise ValidationError("n must be an integer >= 3.")

            if input_data["x_end"] <= input_data["x0"]:
                raise ValidationError("x_end must be greater than x0.")

        return True
