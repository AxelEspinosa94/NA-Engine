import numpy as np

# =========================================================
# CLENSHAW-CURTIS
# =========================================================


def clenshaw_curtis(instance):
    f = instance.f
    a, b = instance.interval
    N = instance.n

    # ---------------------------------------------------------
    # 1. Chebyshev Nodes in [-1, 1]
    # ---------------------------------------------------------
    theta = np.linspace(0, np.pi, N + 1)
    t = np.cos(theta)

    # ---------------------------------------------------------
    # 2. Map nodes to [a, b]
    # ---------------------------------------------------------
    x = (b - a) / 2 * t + (a + b) / 2

    # ---------------------------------------------------------
    # 3. Evaluate the function at the nodes
    # ---------------------------------------------------------
    fvals = f(x)

    # ---------------------------------------------------------
    # 4. DCT-I manual (wo scipy)
    #    a_k = (2/N) * [ f0/2 + fN/2*(-1)^k + sum_{n=1..N-1} f_n cos(n*k*pi/N) ]
    # ---------------------------------------------------------
    k = np.arange(N + 1)
    a_k = np.zeros(N + 1)

    # beginning and end values for the DCT-I formula
    f0_half = 0.5 * fvals[0]
    fN_half = 0.5 * fvals[-1]

    for ki in k:
        cosnk = np.cos((np.arange(1, N) * ki * np.pi) / N)
        inner_sum = np.sum(fvals[1:N] * cosnk)
        a_k[ki] = (2 / N) * (f0_half + fN_half * ((-1) ** ki) + inner_sum)

    # ---------------------------------------------------------
    # 5. Closed formula of Clenshaw–Curtis in [-1, 1]
    #    I = a_0 + sum_{m=1..N/2} 2*a_{2m} / (1 - (2m)^2)
    # ---------------------------------------------------------
    M = N // 2
    I_unit = a_k[0] + np.sum(
        [2 * a_k[2 * m] / (1 - (2 * m) ** 2) for m in range(1, M + 1)]
    )

    # ---------------------------------------------------------
    # 6. Escalate to interval [a, b]
    # ---------------------------------------------------------
    return (b - a) / 2 * I_unit
