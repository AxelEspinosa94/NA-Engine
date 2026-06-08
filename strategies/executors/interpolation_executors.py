import numpy as np
from typing import Any, Dict


class InterpolationExecutor:
    """
    Unified executor for all interpolation methods:
    - lagrange
    - newton
    - spline_cubic
    - hermite
    """

    def run(self, instance):
        mode = instance.calculation_mode

        dispatch = {
            "lagrange": self._run_lagrange,
            "newton": self._run_newton,
            "spline_cubic": self._run_spline,
            "hermite": self._run_hermite,
        }

        if mode not in dispatch:
            raise ValueError(f"Unknown interpolation mode: {mode}")

        return dispatch[mode](instance)

    # ---------------------------------------------------------
    # LAGRANGE
    # ---------------------------------------------------------
    def _run_lagrange(self, instance):
        df = instance.df
        xk = instance.xk

        n = len(df) - 1
        P = 0
        expr = ""

        for i in range(n + 1):
            Li_val, Li_expr = self._lagrange_multiplier(df, i, xk)
            P += Li_val
            expr += Li_expr

        return {
            "value": float(P),
            "expression": expr,
            "table": df
        }

    def _lagrange_multiplier(self, df, i, xk):
        p_i = 1
        expr = ""

        xi = df.iloc[i, 0]
        yi = df.iloc[i, 1]

        for j in range(len(df)):
            if j != i:
                xj = df.iloc[j, 0]
                p_i *= (xk - xj) / (xi - xj)
                expr += f"((x - {xj})/({xi} - {xj})) * "

        expr += f"f({xi})"

        if i < len(df) - 1:
            expr += " + "

        return p_i * yi, expr

    # ---------------------------------------------------------
    # NEWTON
    # ---------------------------------------------------------
    def _run_newton(self, instance):
        df = instance.df
        x = df.iloc[:, 0].values
        y = df.iloc[:, 1].values
        xk = instance.xk

        coef = y.copy()
        n = len(x)

        for j in range(1, n):
            for i in range(n - 1, j - 1, -1):
                coef[i] = (coef[i] - coef[i - 1]) / (x[i] - x[i - j])

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

    # ---------------------------------------------------------
    # SPLINE CUBIC
    # ---------------------------------------------------------
    def _run_spline(self, instance):
        df = instance.df
        x = df.iloc[:, 0].values
        y = df.iloc[:, 1].values
        xk = instance.xk

        n = len(x)
        h = np.diff(x)

        A = np.zeros((n, n))
        b = np.zeros(n)

        A[0, 0] = 1
        A[-1, -1] = 1

        for i in range(1, n - 1):
            A[i, i - 1] = h[i - 1]
            A[i, i] = 2 * (h[i - 1] + h[i])
            A[i, i + 1] = h[i]
            b[i] = 6 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1])

        M = np.linalg.solve(A, b)

        for i in range(n - 1):
            if x[i] <= xk <= x[i + 1]:
                k = i
                break

        hk = x[k + 1] - x[k]

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

    # ---------------------------------------------------------
    # HERMITE
    # ---------------------------------------------------------
    def _run_hermite(self, instance):
        df = instance.df
        x = df.iloc[:, 0].values
        y = df.iloc[:, 1].values
        yp = df.iloc[:, 2].values
        xk = instance.xk

        n = len(x)
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

        m = 2 * n
        for j in range(2, m):
            for i in range(m - j):
                Q[i][j] = (Q[i + 1][j - 1] - Q[i][j - 1]) / (z[i + j] - z[i])

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
