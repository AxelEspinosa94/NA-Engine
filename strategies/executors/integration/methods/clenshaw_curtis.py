import functools

import numpy as np

# =========================================================
# CLENSHAW-CURTIS (nodos y pesos 1D en [-1, 1])
# =========================================================


@functools.lru_cache(maxsize=None)
def _cc_nodes_and_weights(N: int):
    theta = np.pi * np.arange(N + 1) / N
    t = np.cos(theta)

    w = np.zeros(N + 1)
    inner = theta[1:N]  # nodos interiores
    v = np.ones(N - 1)

    if N % 2 == 0:
        w[0] = w[N] = 1 / (N**2 - 1)
        k = np.arange(1, N // 2)
        v -= (2 * np.cos(np.outer(inner, 2 * k)) / (4 * k**2 - 1)).sum(axis=1)
        v -= np.cos(N * inner) / (N**2 - 1)
    else:
        w[0] = w[N] = 1 / N**2
        k = np.arange(1, (N - 1) // 2 + 1)
        v -= (2 * np.cos(np.outer(inner, 2 * k)) / (4 * k**2 - 1)).sum(axis=1)

    w[1:N] = 2 * v / N
    return t, w


# =========================================================
# CLENSHAW-CURTIS Nd (bounds = [[a_1,b_1], [a_2,b_2], ...])
# =========================================================


def clenshaw_curtis(instance):
    f = instance.f
    bounds = instance.bounds
    N = instance.n

    d = len(bounds)
    N_list = [N] * d if isinstance(N, int) else N

    nodes_list = []
    weights_list = []
    for (a, b), Ni in zip(bounds, N_list):
        t, w = _cc_nodes_and_weights(Ni)
        x = (b - a) / 2 * t + (a + b) / 2  # nodos escalados a [a, b]
        nodes_list.append(x)
        weights_list.append((b - a) / 2 * w)  # pesos escalados

    # Caso 1D: igual que tu versión original, sin meshgrid
    if d == 1:
        fvals = f(nodes_list[0])
        return np.sum(weights_list[0] * fvals)

    # Caso Nd: malla tensorial + evaluación vectorizada vía broadcasting
    grids = np.meshgrid(*nodes_list, indexing="ij")
    fvals = f(*grids)

    # Producto tensorial de los pesos de cada eje -> tensor Nd de pesos
    weight_tensor = functools.reduce(np.multiply.outer, weights_list)

    return np.sum(weight_tensor * fvals)
