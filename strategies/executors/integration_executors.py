import numpy as np
import pandas as pd
from core.exceptions import ExecutionError


class IntegrationExecutor:

    def run(self, instance):

        mode = instance.calculation_mode
        a, b = instance.interval
        x = instance.x
        y = instance.y

        # -------------------------
        # DISPATCHER
        # -------------------------
        dispatch = {
            "trapezoid_simple": lambda: self._integrate_rule(x, y, "trapezoid_simple"),
            "trapezoid_composite": lambda: self._integrate_rule(x, y, "trapezoid_composite"),
            "simpson_1_3": lambda: self._integrate_rule(x, y, "simpson_1_3"),
            "simpson_3_8": lambda: self._integrate_rule(x, y, "simpson_3_8"),
            "romberg": lambda: self._romberg(instance),
            "gauss": lambda: self._gauss_legendre(instance)
        }

        if mode not in dispatch:
            raise ExecutionError(f"Unknown integration mode: {mode}")

        value = dispatch[mode]()
        return self._build_payload(instance, value, x, y, mode)

    # =========================================================
    # PAYLOAD BUILDER (UNIFIES OUTPUT LIKE INTERPOLATION)
    # =========================================================
    def _build_payload(self, instance, value, x, y, mode):
        a, b = instance.interval

        # Expression
        expr = f"∫_{a}^{b} f(x) dx ≈ {value:.6g}"

        # Table
        table = pd.DataFrame({"x": x, "y": y})

        # Plot (just the function)
        x_plot = np.linspace(a, b, 200)
        y_plot = instance.f(x_plot)

        return {
            "value": float(value),
            "expression": expr,
            "table": table,
            "x": x_plot.tolist(),
            "y": y_plot.tolist(),
            "x_nodes": x.tolist(),
            "y_nodes": y.tolist(),
            "a": float(a),
            "b": float(b),
            "n": instance.n,
            "calculation_mode": mode
        }

    # =========================================================
    # COMPOSITE RULES (OPTIMIZED DISPATCH)
    # =========================================================
    def _integrate_rule(self, x, y, rule):
        dispatch = {
            "trapezoid_simple": self._trap_simple,
            "trapezoid_composite": self._trap_composite,
            "simpson_1_3": self._simp_1_3,
            "simpson_3_8": self._simp_3_8,
        }

        if rule not in dispatch:
            raise ExecutionError(f"Unknown composite rule: {rule}")

        return dispatch[rule](x, y)

    # -------------------------
    # Individual rule handlers
    # -------------------------

    def _trap_simple(self, x, y):
        n = len(x) - 1
        h = (x[-1] - x[0]) / n
        return h * (y[0] + y[-1]) / 2

    def _trap_composite(self, x, y):
        n = len(x) - 1
        h = (x[-1] - x[0]) / n
        return h * (0.5 * y[0] + y[1:-1].sum() + 0.5 * y[-1])

    def _simp_1_3(self, x, y):
        n = len(x) - 1
        h = (x[-1] - x[0]) / n
        odd = y[1:n:2].sum()
        even = y[2:n-1:2].sum()
        return h / 3 * (y[0] + y[-1] + 4 * odd + 2 * even)

    def _simp_3_8(self, x, y):
        n = len(x) - 1
        h = (x[-1] - x[0]) / n
        sum_3 = y[3:n:3].sum()
        sum_not_3 = y[1:n].sum() - sum_3
        return 3 * h / 8 * (y[0] + y[-1] + 3 * sum_not_3 + 2 * sum_3)


    # =========================================================
    # ROMBERG
    # =========================================================
    def _romberg(self, instance):
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

    # =========================================================
    # GAUSS-LEGENDRE
    # =========================================================
    def _gauss_legendre(self, instance):
        f = instance.f
        a, b = instance.interval
        n = instance.input_data.get("gauss_points", 2)

        Pn = np.polynomial.legendre.Legendre.basis(n)
        t = Pn.roots()
        Pn_der = Pn.deriv()
        w = 2 / ((1 - t**2) * (Pn_der(t)**2))

        x = (b - a) / 2 * t + (a + b) / 2
        return (b - a) / 2 * np.sum(w * f(x))