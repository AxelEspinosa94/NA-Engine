
import sympy as sp
from core.exceptions import ConstructionError


class NonLinearEquation:
    """
    Base class for all nonlinear equation solvers.
    Only supports mode='function'.
    """

    def __init__(self, input_data):
        self.input_data = input_data
        self.mode = input_data.get("mode")
        self.calculation_mode = input_data.get("calculation_mode")

        if self.mode != "function":
            raise ConstructionError("Nonlinear solvers only support mode='function'.")

        # Function f(x)
        func_str = input_data.get("function")
        if not isinstance(func_str, str):
            raise ConstructionError("Function must be a string.")

        x = sp.symbols("x")
        f_sym = sp.sympify(func_str)
        self.f = sp.lambdify(x, f_sym, "numpy")
        self.f_sym = f_sym

        if self.calculation_mode == "fixed_point":
            g_str = input_data.get("g")
            if not isinstance(g_str, str):
                raise ConstructionError("Fixed point method requires g(x).")

            g_sym = sp.sympify(g_str)
            self.g = sp.lambdify(x, g_sym, "numpy")

            # g'(x)
            gprime_sym = sp.diff(g_sym, x)
            self.gprime = sp.lambdify(x, gprime_sym, "numpy")

        # Derivative (only used by Newton)
        self.fprime = None
        if self.calculation_mode == "newton":
            fprime_sym = sp.diff(f_sym, x)
            self.fprime = sp.lambdify(x, fprime_sym, "numpy")

        # Tolerance
        self.tol = input_data.get("tol", 1e-6)
        if not isinstance(self.tol, (float, int)) or self.tol <= 0:
            raise ConstructionError("tol must be a positive number.")

        # Max iterations
        self.max_iter = input_data.get("max_iter", 50)
        if not isinstance(self.max_iter, int) or self.max_iter <= 0:
            raise ConstructionError("max_iter must be a positive integer.")

        # Initial values
        self.x0 = input_data.get("x0")
        self.x1 = input_data.get("x1")
        self.interval = input_data.get("interval")
