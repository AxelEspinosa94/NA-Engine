from typing import List, Union

import numpy as np
import sympy as sp

from core.exceptions import ConstructionError


def build_function(func_str: str, symbols: List[str] = None):
    """
    Build a numpy-vectorized callable from a sympy expression.
    If symbols is None, assume single variable 'x'.
    If symbols provided, create lambdify with those symbols in order.
    """
    if not isinstance(func_str, str) or not func_str.strip():
        raise ConstructionError("Function must be a non-empty string.")

    if symbols is None:
        symbols = ["x"]

    syms = sp.symbols(" ".join(symbols))
    f_sym = sp.sympify(func_str)

    # If constant
    if f_sym.is_Number:
        const = float(f_sym)

        def const_fn(*args):
            # args are arrays; return array of same shape as first arg
            a0 = np.asarray(args[0])
            return np.full_like(a0, const, dtype=float)

        return const_fn

    return sp.lambdify(syms, f_sym, "numpy")


def build_grid(
    f_str: str,
    symbols: List[str] = None,
    bounds: Union[List, List[List]] = None,
    n: Union[int, List[int]] = 1,
):
    f = build_function(f_str, symbols)
    dim = len(symbols) if symbols else 1

    # Normalizar n: mismo número de puntos por eje o uno distinto por eje
    n_list = [n] * dim if isinstance(n, int) else n

    # Construir ejes 1D
    axes = [np.linspace(a, b, ni + 1) for (a, b), ni in zip(bounds, n_list)]

    if dim == 1:
        x = axes[0]
        y = f(x)
        return x, y

    # Malla N-dimensional con indexing='ij' para que los ejes coincidan
    # con el orden de tus variables y con axis=i en la integración posterior
    grids = np.meshgrid(*axes, indexing="ij")
    y = f(*grids)  # broadcasting elemento a elemento gracias a lambdify

    return grids, y
