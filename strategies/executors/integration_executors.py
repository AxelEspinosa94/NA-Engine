import numpy as np
import sympy as sp


class IntegrationExecutor:

    def run(self, instance):

        mode = instance.calculation_mode

        if mode == "romberg":
            value = self._romberg(instance)
            a, b = instance.interval
            return {
                "value": float(value),
                "calculation_mode": mode,
                "a": float(a),
                "b": float(b),
                "n": instance.n
            }

        if mode == "gauss":
            value = self._gauss_legendre(instance)
            a, b = instance.interval
            return {
                "value": float(value),
                "calculation_mode": mode,
                "a": float(a),
                "b": float(b),
                "n": instance.input_data.get("gauss_points", 2)
            }

        # Composite rules
        x = instance.x
        y = instance.y

        dispatch = {
            "trapezoid_simple": lambda: self._integrate_rule(x, y, "trapezoid_simple"),
            "trapezoid_composite": lambda: self._integrate_rule(x, y, "trapezoid_composite"),
            "simpson_1_3": lambda: self._integrate_rule(x, y, "simpson_1_3"),
            "simpson_3_8": lambda: self._integrate_rule(x, y, "simpson_3_8"),
        }

        value = dispatch[mode]()

        return {
            "value": float(value),
            "calculation_mode": mode,
            "a": float(x[0]),
            "b": float(x[-1]),
            "n": instance.n
        }

    # -------------------------
    # Composite rules
    # -------------------------

    def _integrate_rule(self, x, y, rule):
        n = len(x) - 1
        h = (x[-1] - x[0]) / n

        if rule == "trapezoid_simple":
            return h * (y[0] + y[-1]) / 2

        if rule == "trapezoid_composite":
            return h * (0.5 * y[0] + y[1:-1].sum() + 0.5 * y[-1])

        if rule == "simpson_1_3":
            odd = y[1:n:2].sum()
            even = y[2:n-1:2].sum()
            return h / 3 * (y[0] + y[-1] + 4 * odd + 2 * even)

        if rule == "simpson_3_8":
            sum_3 = y[3:n:3].sum()
            sum_not_3 = y[1:n].sum() - sum_3
            return 3 * h / 8 * (y[0] + y[-1] + 3 * sum_not_3 + 2 * sum_3)

    # -------------------------
    # Romberg
    # -------------------------

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

    # -------------------------
    # Gauss-Legendre
    # -------------------------

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
