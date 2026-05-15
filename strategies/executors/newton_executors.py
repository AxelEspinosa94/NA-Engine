from typing import Any, Dict


class NewtonExecutor:
    """
    Executes Newton interpolation using divided differences.
    """

    def run(self, instance):
        df = instance.df
        x = df.iloc[:, 0].values
        y = df.iloc[:, 1].values
        xk = instance.xk

        # Compute divided differences
        coef = y.copy()
        n = len(x)
        for j in range(1, n):
            for i in range(n - 1, j - 1, -1):
                coef[i] = (coef[i] - coef[i - 1]) / (x[i] - x[i - j])

        # Evaluate Newton polynomial
        result = coef[-1]
        for i in range(n - 2, -1, -1):
            result = result * (xk - x[i]) + coef[i]

        return {
            "value": result,
            "coefficients": coef,
            "table": df
        }
