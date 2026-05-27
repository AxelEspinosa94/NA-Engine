import numpy as np

class ODE:
    """
    Constructor for Ordinary Differential Equations.
    Stores input_data only. No validation here.
    """

    def __init__(self, input_data):
        self.input_data = input_data

        # Common fields (no validation here)
        self.f = input_data.get("function")          # f(x, y)
        self.system = input_data.get("system")       # list of functions for systems
        self.x0 = input_data.get("x0")
        self.y0 = input_data.get("y0")
        self.x_end = input_data.get("x_end")
        self.h = input_data.get("h")
        self.calculation_mode = input_data.get("calculation_mode")

        # BVP fields
        self.alpha = input_data.get("alpha", None)  # Boundary condition at x0
        self.beta = input_data.get("beta", None)

        # Shooting initial slope guess
        self.s0 = input_data.get("s0", None)

        # Finite differences grid size
        self.n = input_data.get("n", None)
