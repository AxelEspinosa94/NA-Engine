import pandas as pd
from typing import Dict, Any, Optional
from core.exceptions import ValidationError

class LagrangeMethod:
    """
    Constructor class for Lagrange interpolation.
    Stores input data and prepares the dataframe.
    """

    def __init__(self, input_data: Dict[str, Any], **kwargs):
        """
        Expected input_data:
        {
            "mode": "table" | "function",
            "data": DataFrame | str (function),
            "interval": [a, b],
            "step": float,
            "xk": float
        }
        """
        self.mode: str = input_data.get("mode")
        self.xk: float = input_data.get("xk")
        if self.mode not in ("table", "function"):
            raise ValidationError(
                "Invalid mode. Must be 'table' or 'function'."
            )
        
        if self.mode == "table":
            self.df: pd.DataFrame = input_data["data"]

        elif self.mode == "function":
            func_str: str = input_data["data"]
            a, b = input_data["interval"]
            step = input_data["step"]

            # Build dataframe from function
            import numpy as np
            from sympy import sympify, symbols

            x = symbols("x")
            f = sympify(func_str)

            xs = np.arange(a, b + step, step)
            ys = [float(f.subs(x, val)) for val in xs]

            self.df = pd.DataFrame({"x": xs, "f(x)": ys})

        else:
            raise ValueError("Invalid mode for Lagrange interpolation.")
