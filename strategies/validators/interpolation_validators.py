import pandas as pd
import numpy as np
from typing import Dict, Any
from core.exceptions import ValidationError


class InterpolationValidator:
    """
    General validator for all interpolation methods:
    - lagrange
    - newton
    - spline_cubic
    - hermite
    """

    def validate(self, input_data: Dict[str, Any]) -> bool:
        mode = input_data.get("mode")
        calculation_mode = input_data.get("calculation_mode")

        # -------------------------
        # Validate mode
        # -------------------------
        if mode not in ("table", "function"):
            raise ValidationError("Invalid mode. Must be 'table' or 'function'.")

        # -------------------------
        # TABLE MODE
        # -------------------------
        if mode == "table":
            df = input_data.get("data")

            if not isinstance(df, pd.DataFrame):
                raise ValidationError("Data must be a pandas DataFrame.")

            # Hermite: 3 columns
            if calculation_mode == "hermite":
                if df.shape[1] != 3:
                    raise ValidationError(
                        "Hermite requires exactly 3 columns: x, f(x), f'(x)."
                    )

                x = df.iloc[:, 0].values

                if not np.all(np.diff(x) > 0):
                    raise ValidationError("x values must be strictly increasing for Hermite.")

                if len(x) < 2:
                    raise ValidationError("Hermite interpolation requires at least 2 points.")

                if df.isna().any().any():
                    raise ValidationError("Hermite table contains NaN values.")

                # Numeric types
                for col in df.columns:
                    if not pd.api.types.is_numeric_dtype(df[col]):
                        raise ValidationError(f"Column {col} must contain numeric values.")

            # Other methods: 2 columns
            else:
                if df.shape[1] != 2:
                    raise ValidationError("DataFrame must have exactly 2 columns: x and f(x).")

                if df.isnull().any().any():
                    raise ValidationError("DataFrame contains NaN values.")

                x = df.iloc[:, 0].values
                if not np.all(np.diff(x) > 0):
                    raise ValidationError("x values must be strictly increasing.")

                # Numeric types
                if not pd.api.types.is_numeric_dtype(df.iloc[:, 0]):
                    raise ValidationError("Column x must contain numeric values.")
                if not pd.api.types.is_numeric_dtype(df.iloc[:, 1]):
                    raise ValidationError("Column f(x) must contain numeric values.")

        # -------------------------
        # FUNCTION MODE
        # -------------------------
        if mode == "function":
            func = input_data.get("data") if calculation_mode != "hermite" else input_data.get("function")
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
