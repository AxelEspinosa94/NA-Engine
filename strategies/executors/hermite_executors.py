import numpy as np


class HermiteExecutor:
    """
    Executes Hermite interpolation using the standard
    duplicated-nodes + divided differences matrix Q.
    """

    def run(self, instance):
        df = instance.df
        x = df.iloc[:, 0].values
        y = df.iloc[:, 1].values
        yp = df.iloc[:, 2].values
        xk = instance.xk

        n = len(x)

        # ---------------------------------------------------------
        # 1. Build duplicated nodes z[]
        # ---------------------------------------------------------
        z = np.zeros(2 * n)
        Q = np.zeros((2 * n, 2 * n))

        for i in range(n):
            z[2 * i] = x[i]
            z[2 * i + 1] = x[i]

            Q[2 * i][0] = y[i]
            Q[2 * i + 1][0] = y[i]

            Q[2 * i][1] = yp[i]
            if i == n - 1:
                Q[2 * i + 1][1] = yp[i]
            else:
                Q[2 * i + 1][1] = (y[i + 1] - y[i]) / (x[i + 1] - x[i])

        # ---------------------------------------------------------
        # 2. Fill the rest of Q with divided differences
        # ---------------------------------------------------------
        m = 2 * n
        for j in range(2, m):
            for i in range(m - j):
                Q[i][j] = (Q[i + 1][j - 1] - Q[i][j - 1]) / (z[i + j] - z[i])

        # ---------------------------------------------------------
        # 3. Evaluate using Newton form
        # ---------------------------------------------------------
        result = Q[0][0]
        prod = 1.0

        for j in range(1, m):
            prod *= (xk - z[j - 1])
            result += Q[0][j] * prod

        return {
            "value": float(result),
            "z": z,
            "Q": Q,
            "table": df
        }
