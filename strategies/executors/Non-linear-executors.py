import numpy as np
import pandas as pd
from core.exceptions import ExecutionError


class NonLinearExecutor:

    def run(self, instance):
        mode = instance.calculation_mode

        dispatch = {
            "fixed_point": self._fixed_point,
            "bisection": self._bisection,
            "newton": self._newton,
            "secant": self._secant,
            "false_position": self._false_position,
        }

        if mode not in dispatch:
            raise ExecutionError(f"Executor not implemented for calculation_mode '{mode}'.")

        # Run method → returns (root, iterations, x_list, y_list)
        root, iters, xs, ys = dispatch[mode](instance)

        # Build final payload
        return self._build_output(instance, root, iters, xs, ys)

    # ============================================================
    # Output builder
    # ============================================================

    def _build_output(self, instance, root, iters, xs, ys):
        # Build iteration table
        table = pd.DataFrame({
            "iter": list(range(1, len(xs) + 1)),
            "x": xs,
            "f(x)": ys,
        })

        # Build symbolic expression
        expr = self._build_expr(instance.calculation_mode)

        return {
            "value": float(root),
            "expression": expr,
            "table": table,
            "x": xs,
            "y": ys,
            "matrix": None,
            "vector": xs,
            "calculation_mode": instance.calculation_mode,
            "iterations": iters,
            "tol": instance.tol,
        }

    # ============================================================
    # Symbolic expressions
    # ============================================================

    def _build_expr(self, mode):
        if mode == "newton":
            return "x_{n+1} = x_n - f(x_n)/f'(x_n)"
        if mode == "secant":
            return "x_{n+1} = x_n - f(x_n)(x_n - x_{n-1}) / (f(x_n) - f(x_{n-1}))"
        if mode == "bisection":
            return "c = (a + b) / 2"
        if mode == "false_position":
            return "c = b - f(b)(b - a) / (f(b) - f(a))"
        if mode == "fixed_point":
            return "x_{n+1} = g(x_n)"
        return ""

    # ============================================================
    # Methods
    # ============================================================

    def _fixed_point(self, instance):
        g = instance.g
        gprime = instance.gprime
        x = instance.x0
        tol = instance.tol
        max_iter = instance.max_iter

        xs, ys = [], []

        try:
            if abs(gprime(x)) >= 1:
                raise ExecutionError(
                    f"Fixed point method may diverge: |g'(x0)| = {abs(gprime(x))} ≥ 1"
                )
        except Exception:
            raise ExecutionError("Could not evaluate g'(x0).")

        for i in range(1, max_iter + 1):
            x_next = g(x)

            if not np.isfinite(x_next):
                raise ExecutionError("g(x) produced NaN or infinity.")

            xs.append(x_next)
            ys.append(instance.f(x_next))

            if abs(x_next - x) < tol:
                return x_next, i, xs, ys

            x = x_next

        raise ExecutionError("Fixed point method did not converge within max_iter.")

    def _bisection(self, instance):
        f = instance.f
        a, b = instance.interval
        tol = instance.tol
        max_iter = instance.max_iter

        xs, ys = [], []

        fa = f(a)
        fb = f(b)

        if fa * fb > 0:
            raise ExecutionError(
                f"Bisection requires f(a) and f(b) to have opposite signs. "
                f"f(a)={fa}, f(b)={fb}"
            )

        for i in range(1, max_iter + 1):
            c = (a + b) / 2
            fc = f(c)

            xs.append(c)
            ys.append(fc)

            if abs(fc) < tol or abs(b - a) < tol:
                return c, i, xs, ys

            if fa * fc < 0:
                b = c
                fb = fc
            else:
                a = c
                fa = fc

        raise ExecutionError("Bisection did not converge within max_iter.")

    def _newton(self, instance):
        f = instance.f
        fprime = instance.fprime
        x = instance.x0
        tol = instance.tol
        max_iter = instance.max_iter

        xs, ys = [], []

        for i in range(1, max_iter + 1):
            fx = f(x)
            fpx = fprime(x)

            if abs(fpx) < 1e-14 or not np.isfinite(fpx):
                raise ExecutionError("Newton method failed: derivative is zero or invalid.")

            x_next = x - fx / fpx

            xs.append(x_next)
            ys.append(f(x_next))

            if abs(x_next - x) < tol:
                return x_next, i, xs, ys

            x = x_next

        raise ExecutionError("Newton method did not converge within max_iter.")

    def _secant(self, instance):
        f = instance.f
        x0 = instance.x0
        x1 = instance.x1
        tol = instance.tol
        max_iter = instance.max_iter

        xs, ys = [], []

        for i in range(1, max_iter + 1):
            f0 = f(x0)
            f1 = f(x1)

            denom = f1 - f0
            if denom == 0 or not np.isfinite(denom):
                raise ExecutionError("Secant method failed: zero or invalid denominator.")

            x2 = x1 - f1 * (x1 - x0) / denom

            xs.append(x2)
            ys.append(f(x2))

            if abs(x2 - x1) < tol:
                return x2, i, xs, ys

            x0, x1 = x1, x2

        raise ExecutionError("Secant method did not converge within max_iter.")

    def _false_position(self, instance):
        f = instance.f
        a, b = instance.interval
        tol = instance.tol
        max_iter = instance.max_iter

        xs, ys = [], []

        fa = f(a)
        fb = f(b)

        if fa * fb > 0:
            raise ExecutionError(
                f"False Position requires f(a) and f(b) to have opposite signs. "
                f"f(a)={fa}, f(b)={fb}"
            )

        for i in range(1, max_iter + 1):
            c = b - fb * (b - a) / (fb - fa)
            fc = f(c)

            xs.append(c)
            ys.append(fc)

            if abs(fc) < tol:
                return c, i, xs, ys

            if fa * fc < 0:
                b = c
                fb = fc
            else:
                a = c
                fa = fc

        raise ExecutionError("False Position did not converge within max_iter.")
