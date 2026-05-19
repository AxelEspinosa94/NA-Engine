from typing import Dict, Any
import numpy as np
import sympy as sp
from core.exceptions import ValidationError


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
            raise ValidationError("Integration only supports mode='function'.")

        # Function
        self.func_str = input_data.get("function")
        if not isinstance(self.func_str, str):
            raise ValidationError("Function must be a string.")

        # Interval
        interval = input_data.get("interval")
        if not isinstance(interval, (list, tuple)) or len(interval) != 2:
            raise ValidationError("Function mode requires interval [a, b].")
        self.interval = interval

        # n (subintervals or Romberg depth)
        self.n = input_data.get("n")
        if not isinstance(self.n, int) or self.n <= 0:
            raise ValidationError("Function mode requires positive integer n.")

        # Build sympy function
        x = sp.symbols("x")
        f_sym = sp.sympify(self.func_str)
        self.f = sp.lambdify(x, f_sym, "numpy")

        # Build uniform grid for composite rules
        a, b = self.interval
        self.x = np.linspace(a, b, self.n + 1)
        self.y = self.f(self.x)
