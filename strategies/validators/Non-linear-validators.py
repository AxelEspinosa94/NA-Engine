
from core.exceptions import ValidationError


class NonLinearValidator:

    SUPPORTED = {
        "fixed_point",
        "bisection",
        "newton",
        "secant",
        "false_position",
    }

    def validate(self, input_data):
        mode = input_data.get("mode")
        method = input_data.get("calculation_mode")

        if method not in self.SUPPORTED:
            raise ValidationError(f"Unsupported nonlinear method '{method}'.")

        if mode != "function":
            raise ValidationError("Nonlinear solvers only support mode='function'.")

        # Common: function must exist
        if not isinstance(input_data.get("function"), str):
            raise ValidationError("Function must be a string.")

        # Method-specific validations
        getattr(self, f"_validate_{method}")(input_data)

        return True

    # -------------------------
    # Method-specific validators
    # -------------------------

    def _validate_fixed_point(self, data):
        if not isinstance(data.get("g"), str):
            raise ValidationError("Fixed point method requires g(x).")
        if data.get("x0") is None:
            raise ValidationError("Fixed point method requires x0.")

    def _validate_bisection(self, data):
        interval = data.get("interval")
        if not interval or len(interval) != 2:
            raise ValidationError("Bisection requires interval [a, b].")

    def _validate_false_position(self, data):
        interval = data.get("interval")
        if not interval or len(interval) != 2:
            raise ValidationError("False position requires interval [a, b].")

    def _validate_newton(self, data):
        if data.get("x0") is None:
            raise ValidationError("Newton method requires x0.")

    def _validate_secant(self, data):
        if data.get("x0") is None or data.get("x1") is None:
            raise ValidationError("Secant method requires x0 and x1.")
