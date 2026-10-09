from typing import List

import numpy as np

from app.utils.build_function import build_function


def montecarloSim(
    func_str: str, symbols: List[str], bounds: List, n_samples: int, rng=None
):
    """
    Create a DataFrame with columns X_0..X_{d-1} and f(X).
    - bounds: list of (a,b) for each dimension
    - func_str: string representation of the function
    - n_samples: number of iid uniform samples
    """
    if rng is None:
        rng = np.random.default_rng()

    d = len(bounds)
    # Vectorizado: un solo call a rng.uniform con low/high por eje,
    # en vez de un loop por dimensión
    lows = np.array([a for a, b in bounds])
    highs = np.array([b for a, b in bounds])
    samples = rng.uniform(lows, highs, size=(n_samples, d))

    f = build_function(func_str, symbols)
    args = [samples[:, j] for j in range(d)]
    fx = f(*args)

    return samples, fx
