import pandas as pd
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
            "forward": self.forward,
            "backward": self.backward,
            "central": self.central,
            "richardson": self.richardson,
            "second_forward": self.second_forward,
            "second_central": self.second_central,
            "third_forward": self.third_forward,
            "partial_x": self.partial_x,
            "partial_y": self.partial_y,
        }

        if mode not in dispatch:
            raise ExecutionError(f"Unknown calculation_mode: {mode}")

        raw = dispatch[mode](instance)
        return self._build_output(instance, raw)

    # ============================================================
    # Output Builder (standardized)
    # ============================================================

    def _build_output(self, instance, raw):
        key = list(raw.keys())[0]
        value = float(raw[key])

        # Build expression
        expression = self._build_expr(instance, value)

        f = instance.function
        x0 = float(instance.x)
        h = float(instance.h)
        y0 = instance.y

        # Build nodes used by the method
        x_nodes = []
        y_nodes = []

        for offset in [-h, 0, h, 2*h, 3*h]:
            try:
                x_val = x0 + offset
                y_val = self._eval_function(f, x_val, y0)
                x_nodes.append(x_val)
                y_nodes.append(y_val)
            except Exception:
                pass

        # Plot curve
        x_plot = np.linspace(x0 - 3*h, x0 + 3*h, 200)
        y_plot = [self._eval_function(f, xx, y0) for xx in x_plot]

        # Table
        #table = [{"x": xn, "f(x)": yn} for xn, yn in zip(x_nodes, y_nodes)]
        table = pd.DataFrame({
            "x": x_nodes,
            "f(x)": y_nodes
        })

        return {
            "value": value,
            "expression": expression,
            "table": table,
            "x": x_plot.tolist(),
            "y": y_plot,
            "x_nodes": x_nodes,
            "y_nodes": y_nodes,
            "x0": x0,
            "y0": y0,
            "h": h,
            "calculation_mode": instance.calculation_mode,
        }

    # ============================================================
    # Basic derivatives
    # ============================================================

    def forward(self, instance):
        f = instance.function
        x = instance.x
        h = instance.h

        fx = self._eval_function(f, x)
        fxh = self._eval_function(f, x + h)

        return {"derivative": (fxh - fx) / h}

    def backward(self, instance):
        f = instance.function
        x = instance.x
        h = instance.h

        fx = self._eval_function(f, x)
        fxh = self._eval_function(f, x - h)

        return {"derivative": (fx - fxh) / h}

    def central(self, instance):
        f = instance.function
        x = instance.x
        h = instance.h

        fxh = self._eval_function(f, x + h)
        fxmh = self._eval_function(f, x - h)

        return {"derivative": (fxh - fxmh) / (2 * h)}

    # ============================================================
    # Richardson extrapolation
    # ============================================================

    def richardson(self, instance):
        f = instance.function
        x = instance.x
        h = instance.h
        p = instance.richardson_order

        fxh = self._eval_function(f, x + h)
        fxmh = self._eval_function(f, x - h)
        Dh = (fxh - fxmh) / (2 * h)

        fx2h = self._eval_function(f, x + 2*h)
        fxm2h = self._eval_function(f, x - 2*h)
        D2h = (fx2h - fxm2h) / (4 * h)

        return {"derivative": Dh + (Dh - D2h) / (2**p - 1)}

    # ============================================================
    # Higher-order derivatives
    # ============================================================

    def second_forward(self, instance):
        f = instance.function
        x = instance.x
        h = instance.h

        fx = self._eval_function(f, x)
        fxh = self._eval_function(f, x + h)
        fx2h = self._eval_function(f, x + 2*h)

        return {"second_derivative": (fx2h - 2*fxh + fx) / (h**2)}

    def second_central(self, instance):
        f = instance.function
        x = instance.x
        h = instance.h

        fxh = self._eval_function(f, x + h)
        fx = self._eval_function(f, x)
        fxmh = self._eval_function(f, x - h)

        return {"second_derivative": (fxh - 2*fx + fxmh) / (h**2)}

    def third_forward(self, instance):
        f = instance.function
        x = instance.x
        h = instance.h

        fx = self._eval_function(f, x)
        fxh = self._eval_function(f, x + h)
        fx2h = self._eval_function(f, x + 2*h)
        fx3h = self._eval_function(f, x + 3*h)

        return {"third_derivative": (fx3h - 3*fx2h + 3*fxh - fx) / (h**3)}

    # ============================================================
    # Partial derivatives
    # ============================================================

    def partial_x(self, instance):
        f = instance.function
        x = instance.x
        y = instance.y
        h = instance.h

        fxh = self._eval_function(f, x + h, y)
        fxmh = self._eval_function(f, x - h, y)

        return {"partial_x": (fxh - fxmh) / (2 * h)}

    def partial_y(self, instance):
        f = instance.function
        x = instance.x
        y = instance.y
        h = instance.h

        fyh = self._eval_function(f, x, y + h)
        fymh = self._eval_function(f, x, y - h)

        return {"partial_y": (fyh - fymh) / (2 * h)}

    # ============================================================
    # Build symbolic-like expression for UI
    # ============================================================

    def _build_expr(self, instance, value):
        """
        Builds a human-readable expression for the derivative result.
        Example:
            f(x) = x**2
            f'(x0) = 2*x0 = 6
        """

        f = instance.function
        x0 = instance.x
        y0 = instance.y
        mode = instance.calculation_mode

        # Base function line
        if mode in ["partial_x", "partial_y"]:
            expr = f"f(x, y) = {f}\n"
        else:
            expr = f"f(x) = {f}\n"

        # Derivative notation
        if mode == "forward":
            expr += f"f'(x₀) ≈ {value:.6f}"
        elif mode == "backward":
            expr += f"f'(x₀) ≈ {value:.6f}"
        elif mode == "central":
            expr += f"f'(x₀) ≈ {value:.6f}"
        elif mode == "richardson":
            expr += f"f'(x₀) (Richardson) ≈ {value:.6f}"
        elif mode == "second_forward":
            expr += f"f''(x₀) ≈ {value:.6f}"
        elif mode == "second_central":
            expr += f"f''(x₀) ≈ {value:.6f}"
        elif mode == "third_forward":
            expr += f"f'''(x₀) ≈ {value:.6f}"
        elif mode == "partial_x":
            expr += f"∂f/∂x (x₀, y₀) = ∂f/∂x ({x0}, {y0}) ≈ {value:.6f}"
        elif mode == "partial_y":
            expr += f"∂f/∂y (x₀, y₀) = ∂f/∂y ({x0}, {y0}) ≈ {value:.6f}"
        else:
            expr += f"Derivative ≈ {value:.6f}"

        return expr
