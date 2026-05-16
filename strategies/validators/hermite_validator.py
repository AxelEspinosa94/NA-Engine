import numpy as np
from typing import Dict, Any
from core.exceptions import ValidationError
from strategies.validators.interpolation_validators import InterpolationValidator


class HermiteValidator:
    def validate(self,  input_data: Dict[str, Any]):
        mode = input_data.get("mode")

        # ---------------------------------------------------------
        # MODE FUNCTION
        # ---------------------------------------------------------

        if mode == "function":
            func_str = input_data.get("function")
            interval = input_data.get("interval")
            step = input_data.get("step")

            if not isinstance(func_str, str):
                raise ValidationError("Function must be a string.")

            if not isinstance(interval, (list, tuple)) or len(interval) != 2:
                raise ValidationError("Interval must be a list or tuple of length 2.")

            if not isinstance(step, (int, float)) or step <= 0:
                raise ValidationError("Step must be a positive number.")
        
        # ---------------------------------------------------------
        # MODE TABLE
        # ---------------------------------------------------------
        elif mode == "table":
            df = input_data.get("data")
            x = df.iloc[:, 0].values

            if df.shape[1] != 3:
                raise ValidationError("Hermite table must have 3 columns: x, f(x), f'(x).")

            if not np.all(np.diff(x) > 0):
                raise ValidationError("x values must be strictly increasing for Hermite.")

            if len(x) < 2:
                raise ValidationError("Hermite interpolation requires at least 2 points.")

            if df.isna().any().any():
                raise ValidationError("Hermite table contains NaN values.")
            
        # ---------------------------------------------------------
        # INVALID MODE
        # ---------------------------------------------------------
        else:
            raise ValidationError("Hermite only supports 'table' or 'function' modes.")
        
        return True

