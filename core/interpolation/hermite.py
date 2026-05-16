import pandas as pd
import numpy as np
import sympy as sp
from typing import Dict, List, Any


class HermiteMethod:
    """
    Constructor for Hermite interpolation.
    Supports:
    - mode='function': builds table automatically using sympy
    - mode='table': expects df with columns [x, f(x), f'(x)]
    """

    def __init__(self, input_data: Dict[str, Any], **kwargs):
        self.mode = input_data.get("mode")
        self.input_data = input_data

        if self.mode == "function":
            self.df, self.xk = self._build_from_function()
        elif self.mode == "table":
            self.df, self.xk = self._build_from_table()
        else:
            raise ValueError("Hermite only supports 'function' or 'table' modes.")

    # ---------------------------------------------------------
    # MODE FUNCTION
    # ---------------------------------------------------------
    def _build_from_function(self):
        func_str = self.input_data.get("function")
        interval = self.input_data.get("interval")
        step = self.input_data.get("step")
        xk = self.input_data.get("xk")

        if func_str is None or interval is None or step is None:
            raise ValueError("Function mode requires 'function', 'interval', and 'step'.")

        x = sp.symbols("x")

        try:
            f = sp.sympify(func_str)
        except Exception:
            raise ValueError("Invalid function expression.")

        # Try to compute derivative
        try:
            fprime = sp.diff(f, x)
        except Exception:
            raise ValueError("Could not compute derivative of the function.")

        # Build table
        xs = np.arange(interval[0], interval[1] + step, step)
        fx = [float(f.subs(x, val)) for val in xs]
        fpx = [float(fprime.subs(x, val)) for val in xs]

        df = pd.DataFrame({
            "x": xs,
            "f(x)": fx,
            "f'(x)": fpx
        })

        return df, xk

    # ---------------------------------------------------------
    # MODE TABLE
    # ---------------------------------------------------------
    def _build_from_table(self):
        df = self.input_data.get("data")
        xk = self.input_data.get("xk")

        if not isinstance(df, pd.DataFrame):
            raise ValueError("Data must be a pandas DataFrame.")

        if df.shape[1] != 3:
            raise ValueError("Hermite table must have 3 columns: x, f(x), f'(x).")

        df = df.sort_values(by=df.columns[0]).reset_index(drop=True)

        return df, xk