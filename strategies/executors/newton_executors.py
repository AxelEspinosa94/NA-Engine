from typing import Any, Dict


class NewtonExecutor:
    """
    Executes Newton interpolation using standard divided differences.
    """

    def run(self, instance):
        df = instance.df
        x = df.iloc[:, 0].values
        y = df.iloc[:, 1].values
        xk = instance.xk

        # -----------------------------------------
        # 1. Compute divided differences (in-place)
        # -----------------------------------------
        coef = y.copy()
        n = len(x)

        for j in range(1, n):
            for i in range(n - 1, j - 1, -1):
                coef[i] = (coef[i] - coef[i - 1]) / (x[i] - x[i - j])

        # -----------------------------------------
        # 2. Evaluate Newton polynomial
        # P(x) = c0 + c1(x-x0) + c2(x-x0)(x-x1) + ...
        # -----------------------------------------
        result = coef[0]
        prod = 1.0

        for i in range(1, n):
            prod *= (xk - x[i - 1])
            result += coef[i] * prod

        return {
            "value": float(result),
            "coefficients": coef,
            "table": df
        }