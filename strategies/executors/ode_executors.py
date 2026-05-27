import numpy as np
from core.exceptions import ExecutionError


class ODEExecutors:
    """
    Executors for Ordinary Differential Equations (ODEs).
    Includes IVP, systems, BVP (shooting, finite differences),
    and multistep methods.
    """

    # ============================================================
    # Helper: evaluate f(x, y)
    # ============================================================
    def _eval(self, expr, x, y):
        try:
            return float(eval(expr, {"__builtins__": {}}, {"x": x, "y": y, "np": np}))
        except Exception as e:
            raise ExecutionError(f"Error evaluating function '{expr}': {e}")

    # ============================================================
    # Dispatcher
    # ============================================================
    def run(self, instance):
        mode = instance.input_data["calculation_mode"]

        dispatch = {
            "euler": lambda: self.euler(instance),
            "heun": lambda: self.heun(instance),
            "rk2": lambda: self.rk2(instance),
            "rk4": lambda: self.rk4(instance),
            "rk4_system": lambda: self.rk4_system(instance),
            "shooting": lambda: self.shooting(instance),
            "finite_differences": lambda: self.finite_differences(instance),
            "adams_bashforth_2": lambda: self.adams_bashforth_2(instance),
            "adams_bashforth_3": lambda: self.adams_bashforth_3(instance),
            "adams_moulton_2": lambda: self.adams_moulton_2(instance),
        }

        if mode not in dispatch:
            raise ExecutionError(f"Unknown calculation_mode: {mode}")

        return dispatch[mode]()

    # ============================================================
    # Euler
    # ============================================================
    def euler(self, instance):
        f = instance.input_data["function"]
        x0 = float(instance.input_data["x0"])
        y0 = float(instance.input_data["y0"])
        x_end = float(instance.input_data["x_end"])
        h = float(instance.input_data["h"])

        xs, ys = [x0], [y0]
        x, y = x0, y0

        while x < x_end:
            y = y + h * self._eval(f, x, y)
            x = x + h
            xs.append(x)
            ys.append(y)

        return {"x": xs, "y": ys}

    # ============================================================
    # Heun (Euler mejorado)
    # ============================================================
    def heun(self, instance):
        f = instance.input_data["function"]
        x0 = float(instance.input_data["x0"])
        y0 = float(instance.input_data["y0"])
        x_end = float(instance.input_data["x_end"])
        h = float(instance.input_data["h"])

        xs, ys = [x0], [y0]
        x, y = x0, y0

        while x < x_end:
            k1 = self._eval(f, x, y)
            k2 = self._eval(f, x + h, y + h * k1)
            y = y + (h / 2) * (k1 + k2)
            x = x + h
            xs.append(x)
            ys.append(y)

        return {"x": xs, "y": ys}

    # ============================================================
    # RK2
    # ============================================================
    def rk2(self, instance):
        f = instance.input_data["function"]
        x0 = float(instance.input_data["x0"])
        y0 = float(instance.input_data["y0"])
        x_end = float(instance.input_data["x_end"])
        h = float(instance.input_data["h"])

        xs, ys = [x0], [y0]
        x, y = x0, y0

        while x < x_end:
            k1 = self._eval(f, x, y)
            k2 = self._eval(f, x + h / 2, y + (h / 2) * k1)
            y = y + h * k2
            x = x + h
            xs.append(x)
            ys.append(y)

        return {"x": xs, "y": ys}

    # ============================================================
    # RK4
    # ============================================================
    def rk4(self, instance):
        f = instance.input_data["function"]
        x0 = float(instance.input_data["x0"])
        y0 = float(instance.input_data["y0"])
        x_end = float(instance.input_data["x_end"])
        h = float(instance.input_data["h"])

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

        return {"x": xs, "y": ys}

    # ============================================================
    # RK4 for systems (CORREGIDO)
    # ============================================================
    def rk4_system(self, instance):
        system = instance.input_data["system"]
        x0 = float(instance.input_data["x0"])
        y = np.array(instance.input_data["y0"], dtype=float)
        x_end = float(instance.input_data["x_end"])
        h = float(instance.input_data["h"])

        n = len(system)

        def eval_system(expr, x, y_vec):
            # expr is a string like "y2" or "-y1"
            # we expose y1, y2, ..., yn
            local = {"x": x, "np": np}
            for i in range(n):
                local[f"y{i+1}"] = y_vec[i]
            return float(eval(expr, {"__builtins__": {}}, local))

        xs, ys = [x0], [y.copy()]
        x = x0

        while x < x_end:
            k1 = np.array([eval_system(system[i], x, y) for i in range(n)])
            k2 = np.array([eval_system(system[i], x + h/2, y + h*k1/2) for i in range(n)])
            k3 = np.array([eval_system(system[i], x + h/2, y + h*k2/2) for i in range(n)])
            k4 = np.array([eval_system(system[i], x + h, y + h*k3) for i in range(n)])

            y = y + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
            x = x + h

            xs.append(x)
            ys.append(y.copy())

        return {"x": xs, "y": ys}

    # ============================================================
    # Shooting method (CORREGIDO con Newton)
    # ============================================================
    def shooting(self, instance):
        f = instance.input_data["function"]
        x0 = float(instance.input_data["x0"])
        x_end = float(instance.input_data["x_end"])
        alpha = float(instance.input_data["alpha"])
        beta = float(instance.input_data["beta"])
        s = float(instance.input_data["s0"])
        h = float(instance.input_data["h"])

        def solve_ivp_with_slope(slope):
            x = x0
            y = alpha
            dy = slope

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

            return y

        # Newton iterations
        for _ in range(6):
            y_s = solve_ivp_with_slope(s)
            y_s_eps = solve_ivp_with_slope(s + 1e-6)

            derivative = (y_s_eps - y_s) / 1e-6
            if abs(derivative) < 1e-12:
                break

            s = s - (y_s - beta) / derivative

        return {"y_end": solve_ivp_with_slope(s), "target": beta}

    # ============================================================
    # Finite differences (CORREGIDO para y'' = g(x, y))
    # ============================================================
    def finite_differences(self, instance):
        f = instance.input_data["function"]
        x0 = float(instance.input_data["x0"])
        x_end = float(instance.input_data["x_end"])
        alpha = float(instance.input_data["alpha"])
        beta = float(instance.input_data["beta"])
        n = int(instance.input_data["n"])

        h = (x_end - x0) / n

        A = np.zeros((n-1, n-1))
        b = np.zeros(n-1)

        for i in range(1, n):
            xi = x0 + i*h

            A[i-1, i-1] = -2 - h**2 * self._eval(f, xi, 0)

            if i > 1:
                A[i-1, i-2] = 1
            if i < n-1:
                A[i-1, i] = 1

        b[0] -= alpha
        b[-1] -= beta

        y_inner = np.linalg.solve(A, b)
        y = np.concatenate(([alpha], y_inner, [beta]))

        return {"x": np.linspace(x0, x_end, n+1), "y": y}

    # ============================================================
    # Adams–Bashforth 2
    # ============================================================
    def adams_bashforth_2(self, instance):
        f = instance.input_data["function"]
        x0 = float(instance.input_data["x0"])
        y0 = float(instance.input_data["y0"])
        x_end = float(instance.input_data["x_end"])
        h = float(instance.input_data["h"])

        xs, ys = [x0], [y0]

        k1 = self._eval(f, x0, y0)
        k2 = self._eval(f, x0 + h/2, y0 + h*k1/2)
        y1 = y0 + h*k2

        xs.append(x0 + h)
        ys.append(y1)

        x = x0 + h
        y_prev = y0
        y = y1

        while x < x_end:
            f_prev = self._eval(f, x - h, y_prev)
            f_curr = self._eval(f, x, y)

            y_next = y + h*(3*f_curr - f_prev)/2

            y_prev = y
            y = y_next
            x = x + h

            xs.append(x)
            ys.append(y)

        return {"x": xs, "y": ys}

    # ============================================================
    # Adams–Bashforth 3
    # ============================================================
    def adams_bashforth_3(self, instance):
        f = instance.input_data["function"]
        x0 = float(instance.input_data["x0"])
        y0 = float(instance.input_data["y0"])
        x_end = float(instance.input_data["x_end"])
        h = float(instance.input_data["h"])

        xs, ys = [x0], [y0]

        def rk4_step(x, y):
            k1 = self._eval(f, x, y)
            k2 = self._eval(f, x + h/2, y + h*k1/2)
            k3 = self._eval(f, x + h/2, y + h*k2/2)
            k4 = self._eval(f, x + h, y + h*k3)
            return y + (h/6)*(k1 + 2*k2 + 2*k3 + k4)

        y1 = rk4_step(x0, y0)
        y2 = rk4_step(x0 + h, y1)

        xs += [x0 + h, x0 + 2*h]
        ys += [y1, y2]

        x = x0 + 2*h
        y_prev2 = y0
        y_prev1 = y1
        y = y2

        while x < x_end:
            f0 = self._eval(f, x - 2*h, y_prev2)
            f1 = self._eval(f, x - h, y_prev1)
            f2 = self._eval(f, x, y)

            y_next = y + h*(23*f2 - 16*f1 + 5*f0)/12

            y_prev2 = y_prev1
            y_prev1 = y
            y = y_next
            x = x + h

            xs.append(x)
            ys.append(y)

        return {"x": xs, "y": ys}

    # ============================================================
    # Adams–Moulton 2 (implicit)
    # ============================================================
    def adams_moulton_2(self, instance):
        f = instance.input_data["function"]
        x0 = float(instance.input_data["x0"])
        y0 = float(instance.input_data["y0"])
        x_end = float(instance.input_data["x_end"])
        h = float(instance.input_data["h"])

        xs, ys = [x0], [y0]

        k1 = self._eval(f, x0, y0)
        k2 = self._eval(f, x0 + h/2, y0 + h*k1/2)
        y1 = y0 + h*k2

        xs.append(x0 + h)
        ys.append(y1)

        x = x0 + h
        y_prev = y0
        y = y1

        while x < x_end:
            f_prev = self._eval(f, x - h, y_prev)
            f_curr = self._eval(f, x, y)

            y_pred = y + h*(3*f_curr - f_prev)/2

            y_next = y_pred
            for _ in range(5):
                f_next = self._eval(f, x + h, y_next)
                y_next = y + h*(5*f_next + 8*f_curr - f_prev)/12

            y_prev = y
            y = y_next
            x = x + h

            xs.append(x)
            ys.append(y)

        return {"x": xs, "y": ys}
