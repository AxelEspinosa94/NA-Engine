import pandas as pd
from typing import Dict, Any

from core.exceptions import ValidationError


class InterpolationValidator:
    """
    General validator for all interpolation methods (Lagrange, Newton, Splines, etc.)
    Validates:
    - mode: "table" or "function"
    - DataFrame structure
    - function string
    - interval and step
    - presence of xk
    """

    def validate(self, input_data: Dict[str, Any]) -> bool:
        mode = input_data.get("mode")

        # -------------------------
        # Validate mode
        # -------------------------
        if mode not in ("table", "function"):
            raise ValidationError(
                "Invalid mode. Must be 'table' or 'function'."
            )

        # -------------------------
        # Validate table mode
        # -------------------------
        if mode == "table":
            df = input_data.get("data")

            if not isinstance(df, pd.DataFrame):
                raise ValidationError("Data must be a pandas DataFrame.")

            if df.shape[1] != 2:
                raise ValidationError(
                    "DataFrame must have exactly 2 columns: x and f(x)."
                )

            if df.isnull().any().any():
                raise ValidationError("DataFrame contains NaN values.")

            # Optional: ensure numeric columns
            if not pd.api.types.is_numeric_dtype(df.iloc[:, 0]):
                raise ValidationError("Column x must contain numeric values.")

            if not pd.api.types.is_numeric_dtype(df.iloc[:, 1]):
                raise ValidationError("Column f(x) must contain numeric values.")

        # -------------------------
        # Validate function mode
        # -------------------------
        if mode == "function":
            func = input_data.get("data")
            interval = input_data.get("interval")
            step = input_data.get("step")

            if not isinstance(func, str):
                raise ValidationError("Function must be a string.")

            if not isinstance(interval, (list, tuple)) or len(interval) != 2:
                raise ValidationError("Interval must be a list or tuple [a, b].")

            a, b = interval
            if a >= b:
                raise ValidationError("Interval must satisfy a < b.")

            if step is None or step <= 0:
                raise ValidationError("Step must be a positive number.")

        # -------------------------
        # Validate xk
        # -------------------------
        if "xk" not in input_data:
            raise ValidationError("Missing xk value for interpolation.")

        xk = input_data["xk"]
        if not isinstance(xk, (int, float)):
            raise ValidationError("xk must be a numeric value.")

        return True
