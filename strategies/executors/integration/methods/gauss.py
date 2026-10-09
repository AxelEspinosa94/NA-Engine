import numpy as np

# ======================================================
# GAUSS-LEGENDRE
# ======================================================


def gauss_legendre(instance):
    """
    Tensor-product Gauss-Legendre quadrature.

    Supports:
        - 1D
        - ND
    """

    f = instance.f
    bounds = instance.bounds

    n = instance.input_data.get("gauss_points", 2)

    # ------------------------------------------
    # Legendre roots and weights on [-1,1]
    # ------------------------------------------

    Pn = np.polynomial.legendre.Legendre.basis(n)

    t = Pn.roots()

    Pn_der = Pn.deriv()

    w = 2 / ((1 - t**2) * (Pn_der(t) ** 2))

    # ------------------------------------------
    # Map roots and weights
    # to each interval
    # ------------------------------------------

    nodes = []
    weights = []

    for a, b in bounds:

        nodes.append((b - a) / 2 * t + (a + b) / 2)

        weights.append((b - a) / 2 * w)

    dim = len(bounds)

    # ==========================================
    # 1D
    # ==========================================

    if dim == 1:

        x = nodes[0]

        wx = weights[0]

        return float(np.sum(wx * f(x)))

    # ==========================================
    # ND
    # ==========================================

    grids = np.meshgrid(*nodes, indexing="ij")

    values = f(*grids)

    weight_grids = np.meshgrid(*weights, indexing="ij")

    tensor_weights = np.ones_like(values, dtype=float)

    for wg in weight_grids:
        tensor_weights *= wg

    return float(np.sum(tensor_weights * values))
