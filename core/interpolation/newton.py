import pandas as pd
from typing import Dict, Any
import numpy as np
from sympy import sympify, symbols
from core.exceptions import ValidationError

class NewtonMethod:
    """
    Constructor class for Newton interpolation.
    Prepares the dataframe depending on input mode.
    """

    def __init__(self, input_data: Dict[str, Any], **kwargs):
        self.mode = input_data.get("mode")
        self.xk = input_data.get("xk")
        if self.mode not in ("table", "function"):
            raise ValidationError(
                "Invalid mode. Must be 'table' or 'function'."
            )
        
        if self.mode == "table":
            self.df = input_data["data"]

        elif self.mode == "function":
            func_str = input_data["data"]
            a, b = input_data["interval"]
            step = input_data["step"]

            x = symbols("x")
            f = sympify(func_str)

            xs = np.arange(a, b + step, step)
            ys = [float(f.subs(x, val)) for val in xs]

            self.df = pd.DataFrame({"x": xs, "f(x)": ys})

        else:
            raise ValueError("Invalid mode for Newton interpolation.")
