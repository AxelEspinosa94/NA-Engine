import numpy as np
from core.exceptions import ExecutionError


class ODEExecutor:
    """
    Stage 4 executor for ODE solvers.
    Returns standardized dicts compatible with Renderer + UIContract.
    """

    # ============================================================
    # Helper: safe evaluation of f(x, y)
    # ============================================================
    def _eval(self, expr, x, y):
        try:
            local = {"x": x, "y": y, "np": np}
            return float(eval(expr, {"__builtins__": {}}, local))
        except Exception as e:
            raise ExecutionError(f"Error evaluating function '{expr}': {e}")

    # ============================================================
    # Dispatcher
    # ============================================================
    def run(self, instance):
        mode = instance.calculation_mode

        dispatch = {
            "euler": self._run_euler,
            "heun": self._run_heun,
            "rk2": self._run_rk2,
            "rk4": self._run_rk4,
            "rk4_system": self._run_rk4_system,
            "shooting": self._run_shooting,
            "finite_differences": self._run_finite_diff,
            "adams_bashforth_2": self._run_ab2,
            "adams_bashforth_3": self._run_ab3,
            "adams_moulton_2": self._run_am2,
        }

        if mode not in dispatch:
            raise ExecutionError(f"Unknown calculation_mode: {mode}")

        return dispatch[mode](instance)

    # ============================================================
    # Euler
    # ============================================================
    def _run_euler(self, instance):
        f = instance.f
        x0, y0 = float(instance.x0), float(instance.y0)
        x_end, h = float(instance.x_end), float(instance.h)

        xs, ys = [x0], [y0]
        x, y = x0, y0

        while x < x_end:
            y = y + h * self._eval(f, x, y)
            x = x + h
            xs.append(x)
            ys.append(y)

        return {
            "calculation_mode": "euler",
            "x": xs,
            "y": ys,
            "expression": "y_{n+1} = y_n + h f(x_n, y_n)",
        }

    # ============================================================
    # Heun
    # ============================================================
    def _run_heun(self, instance):
        f = instance.f
        x0, y0 = float(instance.x0), float(instance.y0)
        x_end, h = float(instance.x_end), float(instance.h)

        xs, ys = [x0], [y0]
        x, y = x0, y0

        while x < x_end:
            k1 = self._eval(f, x, y)
            k2 = self._eval(f, x + h, y + h * k1)
            y = y + (h / 2) * (k1 + k2)
            x = x + h
            xs.append(x)
            ys.append(y)

        return {
            "calculation_mode": "heun",
            "x": xs,
            "y": ys,
            "expression": "y_{n+1} = y_n + h/2 (k1 + k2)",
        }

    # ============================================================
    # RK2
    # ============================================================
    def _run_rk2(self, instance):
        f = instance.f
        x0, y0 = float(instance.x0), float(instance.y0)
        x_end, h = float(instance.x_end), float(instance.h)

        xs, ys = [x0], [y0]
        x, y = x0, y0

        while x < x_end:
            k1 = self._eval(f, x, y)
            k2 = self._eval(f, x + h, y + h * k1)
            y = y + h * k2
            x = x + h
            xs.append(x)
            ys.append(y)

        return {
            "calculation_mode": "rk2",
            "x": xs,
            "y": ys,
            "expression": "RK2: y_{n+1} = y_n + h k2",
        }

    # ============================================================
    # RK4
    # ============================================================
    def _run_rk4(self, instance):
        f = instance.f
        x0, y0 = float(instance.x0), float(instance.y0)
        x_end, h = float(instance.x_end), float(instance.h)

        xs, ys = [x0], [y0]
        x, y = x0, y0

        while x < x_end:
            k1 = self._eval(f, x, y)
            k2 = self._eval(f, x + h/2, y + h*k1/2)
            k3 = self._eval(f, x + h/2, y + h*k2/2)
            k4 = self._eval(f, x + h, y + h*k3)

            y = y + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
            x = x + h

            xs.append(x)
            ys.append(y)

        return {
            "calculation_mode": "rk4",
            "x": xs,
            "y": ys,
            "expression": "RK4: y_{n+1} = y_n + h/6 (k1 + 2k2 + 2k3 + k4)",
        }

    # ============================================================
    # RK4 System
    # ============================================================
    def _run_rk4_system(self, instance):
        system = instance.system
        x0 = float(instance.x0)
        y = np.array(instance.y0, dtype=float)
        x_end = float(instance.x_end)
        h = float(instance.h)

        n = len(system)

        def eval_sys(expr, x, y_vec, idx):
            local = {"x": x, "np": np}
            local["y"] = y_vec[idx]
            for i in range(n):
                local[f"y{i+1}"] = y_vec[i]
            return float(eval(expr, {"__builtins__": {}}, local))

        xs, ys = [x0], [y.copy()]
        x = x0

        while x < x_end:
            k1 = np.array([eval_sys(system[i], x, y, i) for i in range(n)])
            k2 = np.array([eval_sys(system[i], x + h/2, y + h*k1/2, i) for i in range(n)])
            k3 = np.array([eval_sys(system[i], x + h/2, y + h*k2/2, i) for i in range(n)])
            k4 = np.array([eval_sys(system[i], x + h, y + h*k3, i) for i in range(n)])

            y = y + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
            x = x + h

            xs.append(x)
            ys.append(y.copy())

        return {
            "calculation_mode": "rk4_system",
            "x": xs,
            "y": ys,
            "expression": "RK4 system: vector form",
        }

    # ============================================================
    # Shooting
    # ============================================================
    def _run_shooting(self, instance):
        f = instance.f
        x0 = float(instance.x0)
        x_end = float(instance.x_end)
        alpha = float(instance.alpha)
        beta = float(instance.beta)
        s0 = float(instance.s0)
        h = float(instance.h)

        def solve_ivp(slope):
            x = x0
            y = alpha
            dy = slope

            xs, ys = [x], [y]

            while x < x_end:
                k1y = dy
                k1s = self._eval(f, x, y)

                k2y = dy + h*k1s/2
                k2s = self._eval(f, x + h/2, y + h*k1y/2)

                k3y = dy + h*k2s/2
                k3s = self._eval(f, x + h/2, y + h*k2y/2)

                k4y = dy + h*k3s
                k4s = self._eval(f, x + h, y + h*k3y)

                y = y + (h/6)*(k1y + 2*k2y + 2*k3y + k4y)
                dy = dy + (h/6)*(k1s + 2*k2s + 2*k3s + k4s)
                x = x + h

                xs.append(x)
                ys.append(y)

            return xs, ys, dy

        xs, ys, dy_final = solve_ivp(s0)

        return {
            "calculation_mode": "shooting",
            "x": xs,
            "y": ys,
            "value": dy_final,
            "expression": "Shooting method (RK4)",
        }

    # ============================================================
    # Finite Differences
    # ============================================================
    def _run_finite_diff(self, instance):
        f = instance.f
        x0 = float(instance.x0)
        x_end = float(instance.x_end)
        alpha = float(instance.alpha)
        beta = float(instance.beta)
        n = int(instance.n)

        h = (x_end - x0) / n

        A = np.zeros((n-1, n-1))
        b = np.zeros(n-1)

        for i in range(1, n):
            xi = x0 + i*h
            A[i-1, i-1] = -2
            if i > 1:
                A[i-1, i-2] = 1
            if i < n-1:
                A[i-1, i] = 1

            b[i-1] = h**2 * self._eval(f, xi, 0)

        b[0] -= alpha
        b[-1] -= beta

        y_inner = np.linalg.solve(A, b)
        y = np.concatenate(([alpha], y_inner, [beta]))

        xs = np.linspace(x0, x_end, n+1)

        return {
            "calculation_mode": "finite_differences",
            "x": xs.tolist(),
            "y": y.tolist(),
            "expression": "Finite differences for y'' = f(x)",
        }

    # ============================================================
    # Adams–Bashforth 2
    # ============================================================
    def _run_ab2(self, instance):
        f = instance.f
        x0, y0 = float(instance.x0), float(instance.y0)
        x_end, h = float(instance.x_end), float(instance.h)

        xs, ys = [x0], [y0]
        x, y = x0, y0

        # bootstrap with Euler
        f0 = self._eval(f, x, y)
        y1 = y + h * f0
        x1 = x + h

        xs.append(x1)
        ys.append(y1)

        x, y = x1, y1

        while x < x_end:
            f_prev = self._eval(f, xs[-2], ys[-2])
            f_curr = self._eval(f, x, y)

            y_next = y + h * (3*f_curr - f_prev) / 2
            x_next = x + h

            xs.append(x_next)
            ys.append(y_next)

            x, y = x_next, y_next

        return {
            "calculation_mode": "adams_bashforth_2",
            "x": xs,
            "y": ys,
            "expression": "AB2: y_{n+1} = y_n + h/2 (3f_n - f_{n-1})",
        }

    # ============================================================
    # Adams–Bashforth 3
    # ============================================================
    def _run_ab3(self, instance):
        f = instance.f
        x0, y0 = float(instance.x0), float(instance.y0)
        x_end, h = float(instance.x_end), float(instance.h)

        xs, ys = [x0], [y0]
        x, y = x0, y0

        # bootstrap with RK2
        k1 = self._eval(f, x, y)
        k2 = self._eval(f, x + h, y + h*k1)
        y1 = y + h * k2
        x1 = x + h

        xs.append(x1)
        ys.append(y1)

        # second bootstrap
        k1 = self._eval(f, x1, y1)
        k2 = self._eval(f, x1 + h, y1 + h*k1)
        y2 = y1 + h * k2
        x2 = x1 + h

        xs.append(x2)
        ys.append(y2)

        x, y = x2, y2

        while x < x_end:
            f_n2 = self._eval(f, xs[-3], ys[-3])
            f_n1 = self._eval(f, xs[-2], ys[-2])
            f_n = self._eval(f, x, y)

            y_next = y + h * (23*f_n - 16*f_n1 + 5*f_n2) / 12
            x_next = x + h

            xs.append(x_next)
            ys.append(y_next)

            x, y = x_next, y_next

        return {
            "calculation_mode": "adams_bashforth_3",
            "x": xs,
            "y": ys,
            "expression": "AB3: y_{n+1} = y_n + h/12 (23f_n - 16f_{n-1} + 5f_{n-2})",
        }

    # ============================================================
    # Adams–Moulton 2 (implicit)
    # ============================================================
    def _run_am2(self, instance):
        f = instance.f
        x0, y0 = float(instance.x0), float(instance.y0)
        x_end, h = float(instance.x_end), float(instance.h)

        xs, ys = [x0], [y0]
        x, y = x0, y0

        # bootstrap with RK2
        k1 = self._eval(f, x, y)
        k2 = self._eval(f, x + h, y + h*k1)
        y1 = y + h * k2
        x1 = x + h

        xs.append(x1)
        ys.append(y1)

        x, y = x1, y1

        while x < x_end:
            f_prev = self._eval(f, xs[-2], ys[-2])
            f_curr = self._eval(f, x, y)

            # Adams–Moulton 2 (implicit)
            y_next = y + h * (f_curr + self._eval(f, x + h, y + h*f_curr)) / 2
            x_next = x + h

            xs.append(x_next)
            ys.append(y_next)

            x, y = x_next, y_next

        return {
            "calculation_mode": "adams_moulton_2",
            "x": xs,
            "y": ys,
            "expression": "AM2: y_{n+1} = y_n + h/2 (f_n + f_{n+1})",
        }
