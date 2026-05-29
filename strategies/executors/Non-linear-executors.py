import numpy as np
from core.exceptions import ValidationError, ExecutionError

class NonLinearExecutor:

    def run(self, instance):
        calculation_mode = instance.calculation_mode

        dispatch = {
            "fixed_point": lambda: self._fixed_point(instance),
            "bisection": lambda: self._bisection(instance),
            "newton": lambda: self._newton(instance),
            "secant": lambda: self._secant(instance),
            "false_position": lambda: self._false_position(instance),
        }

        if calculation_mode not in dispatch:
            raise ValidationError(f"Executor not implemented for calculation_mode '{calculation_mode}'.")

        value, iterations = dispatch[calculation_mode]()

        return {
            "root": float(value),
            "iterations": iterations,
            "calculation_mode": calculation_mode,
            "tol": instance.tol,
        }

    # -------------------------
    # Methods (to implement in step 4–5)
    # -------------------------

    def _fixed_point(self, instance):
        g = instance.g
        gprime = instance.gprime
        x = instance.x0
        tol = instance.tol
        max_iter = instance.max_iter

        # Validación de convergencia local
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

            # Criterio de paro
            if abs(x_next - x) < tol:
                return x_next, i

            x = x_next

        raise ExecutionError("Fixed point method did not converge within max_iter.")

    def _bisection(self, instance):
        f = instance.f
        a, b = instance.interval
        tol = instance.tol
        max_iter = instance.max_iter

        fa = f(a)
        fb = f(b)

        # Validación de cambio de signo
        if fa * fb > 0:
            raise ExecutionError(
                f"Bisection requires f(a) and f(b) to have opposite signs. "
                f"f(a)={fa}, f(b)={fb}"
            )

        for i in range(1, max_iter + 1):
            c = (a + b) / 2
            fc = f(c)

            # Criterio de paro
            if abs(fc) < tol or abs(b - a) < tol:
                return c, i

            # Elegir subintervalo
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

        if x is None:
            raise ExecutionError("Newton method requires x0.")

        for i in range(1, max_iter + 1):

            try:
                fx = f(x)
            except Exception as e:
                raise ExecutionError(f"Newton method failed while evaluating f(x): {e}")

            try:
                fpx = fprime(x)
            except Exception as e:
                raise ExecutionError(f"Newton method failed while evaluating f'(x): {e}")

            # Derivada inválida o cero
            if (not np.isfinite(fpx)) or np.isnan(fpx) or abs(fpx) < 1e-14:
                raise ExecutionError("Newton method failed: derivative is zero or invalid.")

            # Siguiente iteración
            x_next = x - fx / fpx

            # Validación: NaN o infinito
            if (not np.isfinite(x_next)) or np.isnan(x_next):
                raise ExecutionError("Newton method produced NaN or infinity.")

            # Criterio de paro
            if abs(x_next - x) < tol:
                return x_next, i

            x = x_next

        raise ExecutionError("Newton method did not converge within max_iter.")

    def _secant(self, instance):
        f = instance.f
        x0 = instance.x0
        x1 = instance.x1
        tol = instance.tol
        max_iter = instance.max_iter

        if x0 is None or x1 is None:
            raise ExecutionError("Secant method requires x0 and x1.")

        for i in range(1, max_iter + 1):
            f0 = f(x0)
            f1 = f(x1)

            # Validación: denominador no puede ser cero
            denom = f1 - f0
            if denom == 0 or not np.isfinite(denom):
                raise ExecutionError("Secant method failed: zero or invalid denominator.")

            # Fórmula de la secante
            x2 = x1 - f1 * (x1 - x0) / denom

            # Validación: NaN o infinito
            if not np.isfinite(x2):
                raise ExecutionError("Secant method produced NaN or infinity.")

            # Criterio de paro
            if abs(x2 - x1) < tol:
                return x2, i

            # Avanzar iteración
            x0, x1 = x1, x2

        raise ExecutionError("Secant method did not converge within max_iter.")


    def _false_position(self, instance):
        f = instance.f
        a, b = instance.interval
        tol = instance.tol
        max_iter = instance.max_iter

        fa = f(a)
        fb = f(b)

        # Validación: debe haber cambio de signo
        if fa * fb > 0:
            raise ExecutionError(
                f"False Position requires f(a) and f(b) to have opposite signs. "
                f"f(a)={fa}, f(b)={fb}"
            )

        for i in range(1, max_iter + 1):
            # Fórmula de Regula Falsi
            c = b - fb * (b - a) / (fb - fa)
            fc = f(c)

            # Validación: NaN o infinito
            if not np.isfinite(c) or not np.isfinite(fc):
                raise ExecutionError("False Position produced NaN or infinity.")

            # Criterio de paro
            if abs(fc) < tol:
                return c, i

            # Actualizar intervalo conservando el cambio de signo
            if fa * fc < 0:
                b = c
                fb = fc
            else:
                a = c
                fa = fc

        raise ExecutionError("False Position did not converge within max_iter.")

