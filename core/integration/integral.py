from typing import Any, Dict

import numpy as np

from core.exceptions import ConstructionError

from .builder import build_function, build_grid


class Integral:
    """
    Base class for all integration methods.
    Only supports mode='function'.
    """

    def __init__(self, input_data: Dict[str, Any]):
        self.input_data = input_data
        self.mode = input_data.get("mode")
        self.calculation_mode = input_data.get("calculation_mode")

        if self.mode != "function":
            raise ConstructionError("Integration only supports mode='function'.")

        # Function
        self.func_str = input_data.get("function")
        if not isinstance(self.func_str, str):
            raise ConstructionError("Function must be a string.")
        if not self.func_str.strip():
            raise ConstructionError("Function string cannot be empty.")

        # Interval
        interval = input_data.get("interval")
        if not isinstance(interval, (list, tuple)) or len(interval) != 2:
            raise ConstructionError("Function mode requires interval [a, b].")
        try:
            a, b = interval
            if a >= b:
                raise ConstructionError("Interval must satisfy a < b.")
            if not all(isinstance(v, (int, float)) for v in interval):
                raise ConstructionError("Interval values must be numeric.")
        except Exception as e:
            raise ConstructionError(f"Invalid interval format: {e}")

        self.interval = interval

        # n (subintervals or Romberg depth)
        self.n = input_data.get("n")
        if not isinstance(self.n, int) or self.n <= 0:
            raise ConstructionError("Function mode requires positive integer n.")

        # Build sympy function
        self.f = build_function(self.func_str)

        # Build uniform grid for composite rules
        a, b = self.interval
        self.x, self.y = build_grid(self.f, self.interval, self.n)

        if np.any(np.isnan(self.y)):
            raise ConstructionError(
                "Function evaluation produced NaN values on the interval."
            )
