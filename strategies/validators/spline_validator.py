import pandas as pd
from core.exceptions import ValidationError
from strategies.validators.interpolation_validators import InterpolationValidator


class SplineValidator(InterpolationValidator):
    """
    Validator for cubic spline interpolation.
    Extends the general interpolation validator.
    """

    def validate(self, input_data):
        super().validate(input_data)

        df = input_data.get("data")

        x = df.iloc[:, 0].values

        # x must be strictly increasing
        if not all(x[i] < x[i+1] for i in range(len(x)-1)):
            raise ValidationError("x values must be strictly increasing for splines.")

        if len(x) < 3:
            raise ValidationError("At least 3 points are required for cubic splines.")

        return True
