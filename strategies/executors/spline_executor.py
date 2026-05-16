import numpy as np


class SplineExecutor:
    """
    Executes natural cubic spline interpolation.
    """

    def run(self, instance):
        df = instance.df
        x = df.iloc[:, 0].values
        y = df.iloc[:, 1].values
        xk = instance.xk

        n = len(x)

        h = np.diff(x)

        # Step 1: Build the system for M (second derivatives)
        A = np.zeros((n, n))
        b = np.zeros(n)

        # Natural spline boundary conditions
        A[0, 0] = 1
        A[-1, -1] = 1

        # Fill tridiagonal system
        for i in range(1, n - 1):
            A[i, i - 1] = h[i - 1]
            A[i, i] = 2 * (h[i - 1] + h[i])
            A[i, i + 1] = h[i]
            b[i] = 6 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1])

        # Solve for M
        M = np.linalg.solve(A, b)

        # Step 2: Find interval where xk lies
        for i in range(n - 1):
            if x[i] <= xk <= x[i + 1]:
                k = i
                break

        hk = x[k + 1] - x[k]

        # Step 3: Evaluate spline
        term1 = M[k] * (x[k + 1] - xk)**3 / (6 * hk)
        term2 = M[k + 1] * (xk - x[k])**3 / (6 * hk)
        term3 = (y[k] - M[k] * hk**2 / 6) * (x[k + 1] - xk) / hk
        term4 = (y[k + 1] - M[k + 1] * hk**2 / 6) * (xk - x[k]) / hk

        value = term1 + term2 + term3 + term4

        return {
            "value": float(value),
            "M": M,
            "table": df
        }
