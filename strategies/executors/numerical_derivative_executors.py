import numpy as np
from core.exceptions import ExecutionError


class NumericalDerivativeExecutor:
    """
    Executors for numerical derivatives.
    """

    # ============================================================
    # Helper: function evaluation
    # ============================================================

    def _eval_function(self, expr: str, x: float, y: float | None = None) -> float:
        """
        Evaluates the function expression at x (and y if provided).
        Assumes expr is a Python expression in terms of x (and y).
        """
        # Espacio seguro mínimo; puedes reemplazar esto por tu parser centralizado
        local_env = {"x": x, "np": np}
        if y is not None:
            local_env["y"] = y

        try:
            return float(eval(expr, {"__builtins__": {}}, local_env))
        except Exception as e:
            raise ExecutionError(f"Error evaluating function '{expr}': {e}")

    # ============================================================
    # Dispatcher
    # ============================================================

    def run(self, instance):
        mode = instance.input_data.get("calculation_mode")

        dispatch = {
            "forward": lambda: self.forward(instance),
            "backward": lambda: self.backward(instance),
            "central": lambda: self.central(instance),
            "richardson": lambda: self.richardson(instance),
            "second_forward": lambda: self.second_forward(instance),
            "second_central": lambda: self.second_central(instance),
            "third_forward": lambda: self.third_forward(instance),
            "partial_x": lambda: self.partial_x(instance),
            "partial_y": lambda: self.partial_y(instance),
        }

        if mode not in dispatch:
            raise ExecutionError(f"Unknown calculation_mode: {mode}")

        return dispatch[mode]()

    # ============================================================
    # Basic derivatives
    # ============================================================

    def forward(self, instance):
        f = instance.input_data["function"]
        x = float(instance.input_data["x"])
        h = float(instance.input_data["h"])

        fx = self._eval_function(f, x)
        fxh = self._eval_function(f, x + h)

        derivative = (fxh - fx) / h
        return {"derivative": derivative}

    def backward(self, instance):
        f = instance.input_data["function"]
        x = float(instance.input_data["x"])
        h = float(instance.input_data["h"])

        fx = self._eval_function(f, x)
        fxh = self._eval_function(f, x - h)

        derivative = (fx - fxh) / h
        return {"derivative": derivative}

    def central(self, instance):
        f = instance.input_data["function"]
        x = float(instance.input_data["x"])
        h = float(instance.input_data["h"])

        fxh = self._eval_function(f, x + h)
        fxmh = self._eval_function(f, x - h)

        derivative = (fxh - fxmh) / (2 * h)
        return {"derivative": derivative}

    # ============================================================
    # Richardson extrapolation
    # ============================================================

    def richardson(self, instance):
        f = instance.input_data["function"]
        x = float(instance.input_data["x"])
        h = float(instance.input_data["h"])
        p = int(instance.input_data.get("richardson_order", 2))

        # D(h) using central difference
        fxh = self._eval_function(f, x + h)
        fxmh = self._eval_function(f, x - h)
        Dh = (fxh - fxmh) / (2 * h)

        # D(2h)
        fx2h = self._eval_function(f, x + 2 * h)
        fxm2h = self._eval_function(f, x - 2 * h)
        D2h = (fx2h - fxm2h) / (4 * h)

        derivative = Dh + (Dh - D2h) / (2**p - 1)
        return {"derivative": derivative}

    # ============================================================
    # Higher-order derivatives
    # ============================================================

    def second_forward(self, instance):
        f = instance.input_data["function"]
        x = float(instance.input_data["x"])
        h = float(instance.input_data["h"])

        fx = self._eval_function(f, x)
        fxh = self._eval_function(f, x + h)
        fx2h = self._eval_function(f, x + 2 * h)

        derivative = (fx2h - 2 * fxh + fx) / (h**2)
        return {"second_derivative": derivative}

    def second_central(self, instance):
        f = instance.input_data["function"]
        x = float(instance.input_data["x"])
        h = float(instance.input_data["h"])

        fxh = self._eval_function(f, x + h)
        fx = self._eval_function(f, x)
        fxmh = self._eval_function(f, x - h)

        derivative = (fxh - 2 * fx + fxmh) / (h**2)
        return {"second_derivative": derivative}

    def third_forward(self, instance):
        f = instance.input_data["function"]
        x = float(instance.input_data["x"])
        h = float(instance.input_data["h"])

        fx = self._eval_function(f, x)
        fxh = self._eval_function(f, x + h)
        fx2h = self._eval_function(f, x + 2 * h)
        fx3h = self._eval_function(f, x + 3 * h)

        derivative = (fx3h - 3 * fx2h + 3 * fxh - fx) / (h**3)
        return {"third_derivative": derivative}

    # ============================================================
    # Partial derivatives
    # ============================================================

    def partial_x(self, instance):
        f = instance.input_data["function"]
        x = float(instance.input_data["x"])
        y = float(instance.input_data["y"])
        h = float(instance.input_data["h"])

        fxh = self._eval_function(f, x + h, y)
        fxmh = self._eval_function(f, x - h, y)

        derivative = (fxh - fxmh) / (2 * h)
        return {"partial_x": derivative}

    def partial_y(self, instance):
        f = instance.input_data["function"]
        x = float(instance.input_data["x"])
        y = float(instance.input_data["y"])
        h = float(instance.input_data["h"])

        fyh = self._eval_function(f, x, y + h)
        fymh = self._eval_function(f, x, y - h)

        derivative = (fyh - fymh) / (2 * h)
        return {"partial_y": derivative}
