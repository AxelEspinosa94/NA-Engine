import numpy as np
import sympy as sp


def build_function(func_str):
    x = sp.symbols("x")
    f_sym = sp.sympify(func_str)

    # If the function is constant, wrap it
    if f_sym.is_Number:
        const = float(f_sym)
        return lambda x: np.full_like(x, const, dtype=float)

    return sp.lambdify(x, f_sym, "numpy")


def build_grid(f, interval, n):
    a, b = interval
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return x, y
