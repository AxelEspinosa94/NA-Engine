import numpy as np
import sympy as sp

def build_function(func_str):
    x = sp.symbols("x")
    f_sym = sp.sympify(func_str)
    return sp.lambdify(x, f_sym, "numpy")

def build_grid(f, interval, n):
    a, b = interval
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return x, y
