import numpy as np
import pandas as pd


# =========================================================
# PAYLOAD BUILDER (UNIFIES OUTPUT LIKE INTERPOLATION)
# =========================================================
def build_payload(instance, result):
    mode = instance.calculation_mode

    if mode == "montecarlo":
        return _build_montecarlo_payload(instance, result)

    return _build_deterministic_payload(instance, result)


def _build_deterministic_payload(instance, value):

    dim = len(instance.bounds)

    # ====================================
    # 1D
    # ====================================

    if dim == 1:

        a, b = instance.bounds[0]

        table = pd.DataFrame({"x": instance.x, "y": instance.y})

        x_plot = np.linspace(a, b, instance.n)

        y_plot = instance.f(x_plot)

        return {
            "value": float(value),
            "expression": f"∫_{a}^{b} f(x) dx ≈ {value:.6g}",
            "table": table,
            "x": x_plot.tolist(),
            "y": y_plot.tolist(),
            "plot_type": "curve",
            "a": a,
            "b": b,
            "n": instance.n,
            "calculation_mode": instance.calculation_mode,
        }

    # ====================================
    # 2D
    # ====================================

    if dim == 2:

        X, Y = instance.x
        Z = instance.y

        table = pd.DataFrame({"x0": X.ravel(), "x1": Y.ravel(), "f": Z.ravel()})

        return {
            "value": float(value),
            "expression": f"∫∫ f(x,y) dA ≈ {value:.6g}",
            "table": table,
            "plot_type": "surface",
            "x": X.tolist(),
            "y": Y.tolist(),
            "z": Z.tolist(),
            "bounds": instance.bounds,
            "n": instance.n,
            "dimension": dim,
            "plot_type": "volume",
            "calculation_mode": instance.calculation_mode,
        }
    # =====================================================
    # > 3D
    # =====================================================

    return {
        "value": float(value),
        "expression": f"Integral over R^{dim} ≈ {value:.6g}",
        "table": None,
        "bounds": instance.bounds,
        "n": instance.n,
        "dimension": dim,
        "plot_type": None,
        "message": (
            f"Visualization is not supported for " f"{dim}-dimensional functions."
        ),
        "calculation_mode": instance.calculation_mode,
    }


def _build_montecarlo_payload(instance, result):
    samples = instance.x
    fx = instance.y

    dim = samples.shape[1]

    table_data = {f"X_{i}": samples[:, i] for i in range(dim)}

    table_data["f(X)"] = fx

    table = pd.DataFrame(table_data)

    bounds = instance.bounds

    expr = f"∫_D f(x) dV ≈ " f"{result['result']:.6g} " f"± {result['error']:.6g}"

    return {
        "value": float(result["result"]),
        "std_error": float(result["error"]),
        "volume": float(result["volume"]),
        "expression": expr,
        "table": table,
        "n": instance.n,
        "bounds": bounds,
        "dim": dim,
        "calculation_mode": instance.calculation_mode,
    }
