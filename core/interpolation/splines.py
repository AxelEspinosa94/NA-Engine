import pandas as pd
from typing import Dict, Any
import numpy as np
from sympy import sympify, symbols
from core.exceptions import ValidationError


class SplineConstructor():
    """
    Constructor for cubic spline interpolation.
    Only table mode is supported.
    """

    def __init__(self, input_data: Dict[str, Any], **kwargs):
        self.mode = input_data.get("mode")

        if self.mode != "table":
            raise ValueError("Spline interpolation only supports 'table' mode.")

        self.df = input_data.get("data")

        if not isinstance(self.df, pd.DataFrame):
            raise ValueError("Data must be a pandas DataFrame.")

        if self.df.shape[1] != 2:
            raise ValueError("DataFrame must have exactly 2 columns: x and f(x).")

        self.df = self.df.sort_values(by=self.df.columns[0]).reset_index(drop=True)
        self.xk = input_data.get("xk")
        