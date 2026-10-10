import numpy as np

from app.utils.build_function import build_grid

from .simpson_trap import _trap_composite

# ======================================================
# ROMBERG BASE
# ======================================================


def _romberg_base(instance, level):
    """
    Computes R[level, 0] using the composite trapezoidal rule.

    Parameters
    ----------
    instance : Integral
        Constructed Integral instance.

    level : int
        Romberg refinement level.

    Returns
    -------
    float
        Composite trapezoidal approximation.
    """

    n_level = 2**level

    x, y = build_grid(
        f_str=instance.func_str,
        symbols=instance.symbols,
        bounds=instance.bounds,
        n=n_level,
    )

    return _trap_composite(x, y)


# ======================================================
# ROMBERG
# ======================================================


def romberg(instance):
    """
    Romberg integration.

    Supports:
        - 1D
        - ND (through trapezoidal tensor-product integration)

    Notes
    -----
    R[k,0] is obtained from progressively refined
    composite trapezoidal approximations.

    Richardson extrapolation remains unchanged.
    """

    n = instance.n

    R = np.zeros((n + 1, n + 1))

    # First column
    for k in range(n + 1):
        R[k, 0] = _romberg_base(
            instance,
            level=k,
        )

    # Richardson extrapolation
    for k in range(1, n + 1):
        for j in range(1, k + 1):

            R[k, j] = R[k, j - 1] + (R[k, j - 1] - R[k - 1, j - 1]) / (4**j - 1)

    return float(R[n, n])
