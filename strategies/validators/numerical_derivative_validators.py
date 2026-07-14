import numbers
import re
from core.exceptions import ValidationError


class NumericalDerivativeValidator:
    """
    Strict validation for numerical derivative computations.
    """

    SUPPORTED_MODES = [
        "forward",
        "backward",
        "central",
        "richardson",
        "second_forward",
        "second_central",
        "third_forward",
        "partial_x",
        "partial_y",
    ]

    def validate(self, input_data):

        # ───────────────────────────────────────────────
        # calculation_mode
        # ───────────────────────────────────────────────
        mode = input_data.get("calculation_mode")
        if mode is None:
            raise ValidationError("calculation_mode is required for NumericalDerivative.")

        if mode not in self.SUPPORTED_MODES:
            raise ValidationError(f"Unsupported calculation_mode: {mode}")

        # ───────────────────────────────────────────────
        # function
        # ───────────────────────────────────────────────
        func = input_data.get("function")
        if not isinstance(func, str) or not func.strip():
            raise ValidationError("A non-empty 'function' string is required.")

        # Basic syntax check (no weird symbols)
        if re.search(r"[^0-9a-zA-Z+\-*/().\s]", func):
            raise ValidationError("Function contains invalid characters.")

        # ───────────────────────────────────────────────
        # x and h (always required)
        # ───────────────────────────────────────────────
        x = input_data.get("x")
        h = input_data.get("h")

        if not isinstance(x, numbers.Real):
            raise ValidationError("x must be a real number.")

        if not isinstance(h, numbers.Real):
            raise ValidationError("h must be a real number.")

        if h <= 0:
            raise ValidationError("h must be positive.")

        # ───────────────────────────────────────────────
        # y for partial derivatives
        # ───────────────────────────────────────────────
        if mode in ["partial_x", "partial_y"]:
            y = input_data.get("y")
            if not isinstance(y, numbers.Real):
                raise ValidationError("y must be a real number for partial derivatives.")

        # ───────────────────────────────────────────────
        # Validate function variables depending on mode
        # ───────────────────────────────────────────────
        #tokens = re.findall(r"[a-zA-Z]+", func)

        #if mode in ["forward", "backward", "central",
        #            "second_forward", "second_central",
        #            "third_forward", "richardson"]:
        #    allowed = {"x"}
        #elif mode == "partial_x":
        #    allowed = {"x", "y"}   # f(x, y) but derivative wrt x
        #elif mode == "partial_y":
        #    allowed = {"x", "y"}   # f(x, y) but derivative wrt y

        #for t in tokens:
        #    if t not in allowed:
        #        raise ValidationError(
        #            f"Invalid variable '{t}' in function for mode '{mode}'. "
        #            f"Allowed variables: {allowed}."
        #        )

        # ───────────────────────────────────────────────
        # Richardson order
        # ───────────────────────────────────────────────
        if mode == "richardson":
            p = input_data.get("richardson_order", 2)
            if not isinstance(p, int) or p <= 0:
                raise ValidationError("richardson_order must be a positive integer.")

        return True
