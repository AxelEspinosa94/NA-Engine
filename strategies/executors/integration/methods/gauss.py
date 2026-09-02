import numpy as np


# =========================================================
# GAUSS-LEGENDRE
# =========================================================
def gauss_legendre(instance):
    f = instance.f
    a, b = instance.interval
    n = instance.input_data.get("gauss_points", 2)

    Pn = np.polynomial.legendre.Legendre.basis(n)
    t = Pn.roots()
    Pn_der = Pn.deriv()
    w = 2 / ((1 - t**2) * (Pn_der(t) ** 2))

    x = (b - a) / 2 * t + (a + b) / 2
    return (b - a) / 2 * np.sum(w * f(x))
