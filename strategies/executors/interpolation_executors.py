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

        # Evaluar el polinomio en un rango para graficar
        x_nodes = df.iloc[:, 0].values
        x_plot  = np.linspace(x_nodes.min(), x_nodes.max(), 200)
        y_plot  = np.array([self._eval_lagrange(df, x) for x in x_plot])

        return {
            "value":      float(P),
            "expression": "L(x) = " + expr,
            "table":      df,
            "x":          x_plot.tolist(),
            "y":          y_plot.tolist(),
            "x_nodes":    x_nodes.tolist(),
            "y_nodes":    df.iloc[:, 1].values.tolist(),
        }

    def _eval_lagrange(self, df, x):
        """Evalúa el polinomio de Lagrange en un punto x."""
        n = len(df)
        P = 0
        for i in range(n):
            xi = df.iloc[i, 0]
            yi = df.iloc[i, 1]
            Li = 1
            for j in range(n):
                if j != i:
                    xj = df.iloc[j, 0]
                    Li *= (x - xj) / (xi - xj)
            P += Li * yi
        return float(P)

    def _lagrange_multiplier(self, df, i, xk):
        p_i = 1
        expr_parts = []

        xi = df.iloc[i, 0]
        yi = df.iloc[i, 1]

        for j in range(len(df)):
            if j != i:
                xj = df.iloc[j, 0]
                p_i *= (xk - xj) / (xi - xj)
                expr_parts.append(f"(x - {xj:.4g}) / ({xi:.4g} - {xj:.4g})")

        # Multiplicar por yi explícito en lugar de f(xi)
        factor = " * ".join(expr_parts)
        expr = f"{yi:.4g} * {factor}"

        return p_i * yi, expr

    # ---------------------------------------------------------
    # NEWTON
    # ---------------------------------------------------------
    def _run_newton(self, instance):
        df = instance.df
        x = df.iloc[:, 0].values
        y = df.iloc[:, 1].values
        xk = instance.xk

        coef = y.copy().astype(float)
        n = len(x)

        # Diferencias divididas
        for j in range(1, n):
            for i in range(n - 1, j - 1, -1):
                coef[i] = (coef[i] - coef[i - 1]) / (x[i] - x[i - j])

        # Evaluación en xk
        result = coef[0]
        prod = 1.0
        for i in range(1, n):
            prod *= (xk - x[i - 1])
            result += coef[i] * prod

        # Expresión simbólica
        expr = self._newton_expression(coef, x)

        # Puntos para graficar
        x_plot = np.linspace(x.min(), x.max(), 200)
        y_plot = np.array([self._eval_newton(coef, x, xi) for xi in x_plot])

        return {
            "value":      float(result),
            "expression": expr,
            "table":      df,
            "x":          x_plot.tolist(),
            "y":          y_plot.tolist(),
            "x_nodes":    x.tolist(),
            "y_nodes":    y.tolist(),
        }

    def _newton_expression(self, coef, x) -> str:
        """Construye la expresión simbólica del polinomio de Newton."""
        terms = [f"{coef[0]:.4g}"]

        for i in range(1, len(coef)):
            # término acumulado: (x - x0)(x - x1)...(x - x_{i-1})
            factors = " * ".join(f"(x - {x[j]:.4g})" for j in range(i))
            sign    = "+" if coef[i] >= 0 else "-"
            terms.append(f"{sign} {abs(coef[i]):.4g} * {factors}")

        return "P(x) = "+ " ".join(terms)

    def _eval_newton(self, coef, x_nodes, xk) -> float:
        """Evalúa el polinomio de Newton en un punto xk."""
        result = coef[0]
        prod   = 1.0
        for i in range(1, len(coef)):
            prod   *= (xk - x_nodes[i - 1])
            result += coef[i] * prod
        return float(result)

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

        # Sistema tridiagonal
        A = np.zeros((n, n))
        b = np.zeros(n)
        A[0, 0] = 1
        A[-1, -1] = 1

        for i in range(1, n - 1):
            A[i, i - 1] = h[i - 1]
            A[i, i]     = 2 * (h[i - 1] + h[i])
            A[i, i + 1] = h[i]
            b[i] = 6 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1])

        M = np.linalg.solve(A, b)

        # Tramo donde cae xk
        k = next(i for i in range(n - 1) if x[i] <= xk <= x[i + 1])
        hk = x[k + 1] - x[k]

        term1 = M[k]     * (x[k + 1] - xk)**3 / (6 * hk)
        term2 = M[k + 1] * (xk - x[k])**3     / (6 * hk)
        term3 = (y[k]     - M[k]     * hk**2 / 6) * (x[k + 1] - xk) / hk
        term4 = (y[k + 1] - M[k + 1] * hk**2 / 6) * (xk - x[k])     / hk

        value = term1 + term2 + term3 + term4

        # Expresión del tramo activo
        expr = self._spline_expression(M, x, y, k, hk)

        # Gráfica: evaluar cada tramo
        x_plot, y_plot = self._eval_spline_curve(M, x, y, h)

        return {
            "value":      float(value),
            "expression": expr,
            "table":      df,
            "x":          x_plot,
            "y":          y_plot,
            "x_nodes":    x.tolist(),
            "y_nodes":    y.tolist(),
        }

    def _spline_expression(self, M, x, y, k, hk) -> str:
        """Expresión del spline cúbico en el tramo k."""
        a = M[k]     / (6 * hk)
        b = M[k + 1] / (6 * hk)
        c = y[k]     / hk - M[k]     * hk / 6
        d = y[k + 1] / hk - M[k + 1] * hk / 6

        return (
            f"S(x) en [{x[k]:.4g}, {x[k+1]:.4g}] =\n"
            f"  {a:.4g} * (x - {x[k+1]:.4g})³\n"
            f"+ {b:.4g} * (x - {x[k]:.4g})³\n"
            f"+ {c:.4g} * (x - {x[k+1]:.4g})\n"  
            f"+ {d:.4g} * (x - {x[k]:.4g})"
        )

    def _eval_spline_curve(self, M, x, y, h) -> tuple:
        """Evalúa la curva completa del spline para graficar."""
        x_plot = []
        y_plot = []

        for k in range(len(x) - 1):
            hk      = h[k]
            x_tramo = np.linspace(x[k], x[k + 1], 50)

            for xk in x_tramo:
                t1 = M[k]     * (x[k + 1] - xk)**3 / (6 * hk)
                t2 = M[k + 1] * (xk - x[k])**3     / (6 * hk)
                t3 = (y[k]     - M[k]     * hk**2 / 6) * (x[k + 1] - xk) / hk
                t4 = (y[k + 1] - M[k + 1] * hk**2 / 6) * (xk - x[k])     / hk
                x_plot.append(float(xk))
                y_plot.append(float(t1 + t2 + t3 + t4))

        return x_plot, y_plot

    # ---------------------------------------------------------
    # HERMITE
    # ---------------------------------------------------------
    def _run_hermite(self, instance):
        df = instance.df
        x  = df.iloc[:, 0].values
        y  = df.iloc[:, 1].values
        yp = df.iloc[:, 2].values
        xk = instance.xk

        n = len(x)
        z = np.zeros(2 * n)
        Q = np.zeros((2 * n, 2 * n))

        for i in range(n):
            z[2 * i]     = x[i]
            z[2 * i + 1] = x[i]

            Q[2 * i][0]     = y[i]
            Q[2 * i + 1][0] = y[i]
            Q[2 * i + 1][1] = yp[i]

            if i < n - 1:
                Q[2 * i + 1][1] = (y[i + 1] - y[i]) / (x[i + 1] - x[i])

        m = 2 * n
        for j in range(2, m):
            for i in range(m - j):
                Q[i][j] = (Q[i + 1][j - 1] - Q[i][j - 1]) / (z[i + j] - z[i])

        # Evaluación en xk
        result = Q[0][0]
        prod   = 1.0
        for j in range(1, m):
            prod   *= (xk - z[j - 1])
            result += Q[0][j] * prod

        # Expresión simbólica
        expr = self._hermite_expression(Q, z, m)

        # Gráfica
        x_plot = np.linspace(x.min(), x.max(), 200)
        y_plot = np.array([self._eval_hermite(Q, z, m, xi) for xi in x_plot])

        return {
            "value":      float(result),
            "expression": expr,
            "table":      df,
            "x":          x_plot.tolist(),
            "y":          y_plot.tolist(),
            "x_nodes":    x.tolist(),
            "y_nodes":    y.tolist(),
        }

    def _hermite_expression(self, Q, z, m) -> str:
        """Expresión simbólica del polinomio de Hermite."""
        terms = [f"H(x) = {Q[0][0]:.4g}"]

        for j in range(1, m):
            factors = " * ".join(f"(x - {z[k]:.4g})" for k in range(j))
            sign    = "+" if Q[0][j] >= 0 else "-"
            terms.append(f"  {sign} {abs(Q[0][j]):.4g} * {factors}")

        return " ".join(terms)

    def _eval_hermite(self, Q, z, m, xk) -> float:
        """Evalúa el polinomio de Hermite en un punto xk."""
        result = Q[0][0]
        prod   = 1.0
        for j in range(1, m):
            prod   *= (xk - z[j - 1])
            result += Q[0][j] * prod
        return float(result)