import pandas as pd
import numpy as np
import sympy as sp
from typing import Dict, Any
from core.exceptions import ConstructionError


class Interpolation:
    """
    Unified constructor for interpolation methods:
    - lagrange
    - newton
    - spline_cubic
    - hermite
    """

    def __init__(self, input_data: Dict[str, Any], **kwargs):
        self.calculation_mode: str = input_data.get("calculation_mode")
        self.mode: str = input_data.get("mode")
        self.xk: float = input_data.get("xk")

        if self.mode not in ("table", "function"):
            raise ConstructionError("Invalid mode. Must be 'table' or 'function'.")

        # Dispatch by calculation_mode
        if self.calculation_mode == "hermite":
            self.df = self._build_hermite(input_data)

        else:
            # Default interpolation builder (lagrange, newton, spline)
            self.df = self._build_standard(input_data)

        # Spline-specific ordering
        if self.calculation_mode == "spline_cubic":
            if self.df.shape[1] != 2:
                raise ConstructionError("Spline requires exactly 2 columns: x and f(x).")
            self.df = self.df.sort_values(by=self.df.columns[0]).reset_index(drop=True)

    # ---------------------------------------------------------
    # Standard interpolation (lagrange, newton)
    # ---------------------------------------------------------
    def _build_standard(self, input_data):
        if self.mode == "table":
            df = input_data["data"]
            if not isinstance(df, pd.DataFrame):
                raise ConstructionError("Data must be a pandas DataFrame.")
            return df

        elif self.mode == "function":
            func_str: str = input_data["data"]
            a, b = input_data["interval"]
            step = input_data["step"]

            x = sp.symbols("x")
            try:
                f = sp.sympify(func_str)
            except Exception:
                raise ConstructionError("Invalid function expression.")

            xs = np.arange(a, b + step, step)
            ys = [float(f.subs(x, val)) for val in xs]

            return pd.DataFrame({"x": xs, "f(x)": ys})

        raise ConstructionError("Invalid mode for interpolation.")

    # ---------------------------------------------------------
    # Hermite interpolation builder
    # ---------------------------------------------------------
    def _build_hermite(self, input_data):
        if self.mode == "function":
            return self._build_hermite_from_function(input_data)

        elif self.mode == "table":
            return self._build_hermite_from_table(input_data)

        raise ConstructionError("Hermite only supports 'function' or 'table' modes.")

    def _build_hermite_from_function(self, input_data):
        func_str = input_data.get("function")
        interval = input_data.get("interval")
        step = input_data.get("step")

        if func_str is None or interval is None or step is None:
            raise ConstructionError("Function mode requires 'function', 'interval', and 'step'.")

        x = sp.symbols("x")

        try:
            f = sp.sympify(func_str)
        except Exception:
            raise ConstructionError("Invalid function expression.")

        # Compute derivative
        try:
            fprime = sp.diff(f, x)
        except Exception:
            raise ConstructionError("Could not compute derivative of the function.")

        xs = np.arange(interval[0], interval[1] + step, step)
        fx = [float(f.subs(x, val)) for val in xs]
        fpx = [float(fprime.subs(x, val)) for val in xs]

        return pd.DataFrame({
            "x": xs,
            "f(x)": fx,
            "f'(x)": fpx
        })

    def _build_hermite_from_table(self, input_data):
        df = input_data.get("data")

        if not isinstance(df, pd.DataFrame):
            raise ConstructionError("Data must be a pandas DataFrame.")

        if df.shape[1] != 3:
            raise ConstructionError("Hermite table must have 3 columns: x, f(x), f'(x).")

        return df.sort_values(by=df.columns[0]).reset_index(drop=True)
