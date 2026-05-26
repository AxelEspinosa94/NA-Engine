import numpy as np


class NumericalDerivative:
    """
    Constructor for numerical derivatives.
    This class ONLY stores input_data and exposes attributes
    used by the validator and executor.
    """

    def __init__(self, input_data):
        self.input_data = input_data

        # Optional / common fields (no validación aquí)
        self.function = input_data.get("function")      # str
        self.x = input_data.get("x")                    # float
        self.y = input_data.get("y")                    # float (for partials)
        self.h = input_data.get("h")                    # float
        self.calculation_mode = input_data.get("calculation_mode")
        if "richardson" in input_data:
            self.richardson_order = input_data.get("richardson_order", 2)
