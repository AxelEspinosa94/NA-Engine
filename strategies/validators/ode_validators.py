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

        # ---------------------------
        # IVP fields
        # ---------------------------
        if mode in ["euler", "heun", "rk2", "rk4", "adams_bashforth_2",
                    "adams_bashforth_3", "adams_moulton_2"]:

            if not isinstance(input_data.get("function"), str):
                raise ValidationError("function must be a string.")

            if not isinstance(input_data.get("x0"), numbers.Real):
                raise ValidationError("x0 must be a real number.")

            if not isinstance(input_data.get("y0"), numbers.Real):
                raise ValidationError("y0 must be a real number.")

            if not isinstance(input_data.get("x_end"), numbers.Real):
                raise ValidationError("x_end must be a real number.")

            if not isinstance(input_data.get("h"), numbers.Real) or input_data["h"] <= 0:
                raise ValidationError("h must be a positive real number.")

        # ---------------------------
        # System of ODEs
        # ---------------------------
        if mode == "rk4_system":
            system = input_data.get("system")
            if not isinstance(system, list) or not all(isinstance(f, str) for f in system):
                raise ValidationError("system must be a list of function strings.")

            if not isinstance(input_data.get("y0"), list):
                raise ValidationError("y0 must be a list for system ODEs.")

        # ---------------------------
        # Shooting method (BVP)
        # ---------------------------
        if mode == "shooting":
            for key in ["function", "x0", "x_end", "alpha", "beta", "s0", "h"]:
                if key not in input_data:
                    raise ValidationError(f"{key} is required for shooting method.")

        # ---------------------------
        # Finite differences (BVP)
        # ---------------------------
        if mode == "finite_differences":
            if not isinstance(input_data.get("n"), int) or input_data["n"] < 3:
                raise ValidationError("n must be an integer >= 3 for finite differences.")

            for key in ["function", "x0", "x_end", "alpha", "beta"]:
                if key not in input_data:
                    raise ValidationError(f"{key} is required for finite differences.")

        return True
