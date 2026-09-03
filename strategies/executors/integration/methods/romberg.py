import numpy as np


# =========================================================
# ROMBERG
# =========================================================
def romberg(instance):
    f = instance.f
    a, b = instance.interval
    n = instance.n

    R = np.zeros((n + 1, n + 1))

    h = b - a

    R[0, 0] = h * (f(a) + f(b)) / 2

    for k in range(1, n + 1):
        h /= 2
        midpoints = a + h * np.arange(1, 2**k, 2)
        R[k, 0] = 0.5 * R[k - 1, 0] + h * np.sum(f(midpoints))
        for j in range(1, k + 1):
            R[k, j] = R[k, j - 1] + (R[k, j - 1] - R[k - 1, j - 1]) / (4**j - 1)

    return R[n, n]
