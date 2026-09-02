import numpy as np
import pandas as pd


# =========================================================
# PAYLOAD BUILDER (UNIFIES OUTPUT LIKE INTERPOLATION)
# =========================================================
def build_payload(instance, value):
    mode = instance.calculation_mode
    a, b = instance.interval
    x = instance.x
    y = instance.y

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
        "calculation_mode": mode,
    }
