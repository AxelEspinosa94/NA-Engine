from typing import Dict, Any
from core.exceptions import ValidationError


class IntegrationValidator:

    SUPPORTED_MODES = {
        "trapezoid_simple",
        "trapezoid_composite",
        "simpson_1_3",
        "simpson_3_8",
        "romberg",
        "gauss"
    }

    def validate(self, input_data: Dict[str, Any]) -> bool:
        mode = input_data.get("mode")
        calculation_mode = input_data.get("calculation_mode")

        if calculation_mode not in self.SUPPORTED_MODES:
            raise ValidationError("Unsupported calculation_mode.")

        # Only function mode allowed
        if mode != "function":
            raise ValidationError("Integration only supports mode='function'.")

        # Function
        if not isinstance(input_data.get("function"), str):
            raise ValidationError("Function must be a string.")

        # Interval
        interval = input_data.get("interval")
        if not isinstance(interval, (list, tuple)) or len(interval) != 2:
            raise ValidationError("Function mode requires interval [a, b].")

        # n
        n = input_data.get("n")
        if not isinstance(n, int) or n <= 0:
            raise ValidationError("Function mode requires positive integer n.")

        # Method-specific constraints
        self._validate_n_for_mode(n, calculation_mode)

        # Gauss-specific
        if calculation_mode == "gauss":
            gp = input_data.get("gauss_points", 2)
            if gp > 50:
                raise ValidationError("Gauss-Legendre unstable for n > 50.")

        return True

    def _validate_n_for_mode(self, n: int, mode: str):
        rules = {
            "trapezoid_simple": lambda n: n == 1,
            "trapezoid_composite": lambda n: n >= 1,
            "simpson_1_3": lambda n: n % 2 == 0,
            "simpson_3_8": lambda n: n % 3 == 0,
            "romberg": lambda n: True,
            "gauss": lambda n: True,
        }

        if not rules[mode](n):
            messages = {
                "trapezoid_simple": "Trapezoid simple requires n = 1.",
                "trapezoid_composite": "Trapezoid composite requires n >= 1.",
                "simpson_1_3": "Simpson 1/3 requires even n.",
                "simpson_3_8": "Simpson 3/8 requires n multiple of 3.",
            }
            raise ValidationError(messages.get(mode, "Invalid n."))
