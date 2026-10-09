import numpy as np

from core.exceptions import ExecutionError


def integrate_rule(instance):
    rule = instance.calculation_mode
    x = instance.x
    y = instance.y

    dispatch = {
        "trapezoid_simple": _trap_simple,
        "trapezoid_composite": _trap_composite,
        "simpson_1_3": _simp_1_3,
        "simpson_3_8": _simp_3_8,
    }

    if rule not in dispatch:
        raise ExecutionError(f"Unknown composite rule: {rule}")

    return dispatch[rule](x, y)


# ======================================================
# Helpers
# ======================================================


def _is_nd(y):
    return hasattr(y, "ndim") and y.ndim > 1


def _axis_h(x, axis):
    grid = np.asarray(x[axis])

    if grid.ndim == 1:
        # x[axis] ya es el vector 1D del eje
        return grid[1] - grid[0]

    # x[axis] es el meshgrid ND completo para ese eje (salida de np.meshgrid
    # con indexing='ij'): extraemos el vector 1D fijando todos los demás
    # índices en 0, variando solo a lo largo de `axis`.
    idx = [0] * grid.ndim
    idx[axis] = slice(None)
    axis_values = grid[tuple(idx)]

    return axis_values[1] - axis_values[0]


def _collapse_axis_trap(values, h, axis):
    n = values.shape[axis] - 1

    weights = np.ones(n + 1)
    weights[0] = 0.5
    weights[-1] = 0.5

    shape = [1] * values.ndim
    shape[axis] = n + 1
    weights = weights.reshape(shape)

    return h * np.sum(values * weights, axis=axis)


def _collapse_axis_simpson(values, h, axis):
    n = values.shape[axis] - 1

    if n % 2 != 0:
        raise ExecutionError(
            f"Simpson 1/3 requiere un numero par de subintervalos en el eje {axis} "
            f"(shape[{axis}]={n + 1}, n={n})."
        )

    weights = np.ones(n + 1)
    idx = np.arange(1, n)
    weights[idx] = np.where(idx % 2 == 1, 4, 2)

    shape = [1] * values.ndim
    shape[axis] = n + 1
    weights = weights.reshape(shape)

    return h / 3 * np.sum(values * weights, axis=axis)


def _collapse_axis_simpson_38(values, h, axis):
    n = values.shape[axis] - 1

    if n % 3 != 0:
        raise ExecutionError(
            f"Simpson 3/8 requiere subintervalos multiplo de 3 en el eje {axis} "
            f"(shape[{axis}]={n + 1}, n={n})."
        )

    weights = np.ones(n + 1)
    idx = np.arange(1, n)
    weights[idx] = np.where(idx % 3 == 0, 2, 3)

    shape = [1] * values.ndim
    shape[axis] = n + 1
    weights = weights.reshape(shape)

    return 3 * h / 8 * np.sum(values * weights, axis=axis)


# ======================================================
# TRAPEZOID SIMPLE
# ======================================================


def _trap_simple(x, y):
    # ----------------------
    # 1D
    # ----------------------
    if not _is_nd(y):
        n = len(x) - 1
        h = (x[-1] - x[0]) / n
        return h * (y[0] + y[-1]) / 2

    # ----------------------
    # ND (producto tensorial del trapecio de un solo panel por eje)
    # ----------------------
    for axis in range(y.ndim):
        if y.shape[axis] != 2:
            raise ExecutionError(
                "Trapezoid simple en ND requiere exactamente 2 puntos por eje "
                f"(eje {axis} tiene {y.shape[axis]}). Usa trapezoid_composite "
                "para mallas mas finas."
            )

    result = y.copy()
    for axis in reversed(range(y.ndim)):
        h = _axis_h(x, axis)
        result = _collapse_axis_trap(result, h, axis)

    return float(result)


# ======================================================
# TRAPEZOID COMPOSITE
# ======================================================


def _trap_composite(x, y):
    # ----------------------
    # 1D
    # ----------------------
    if not _is_nd(y):
        n = len(x) - 1
        h = (x[-1] - x[0]) / n
        return h * (0.5 * y[0] + y[1:-1].sum() + 0.5 * y[-1])

    # ----------------------
    # ND
    # ----------------------
    result = y.copy()
    for axis in reversed(range(y.ndim)):
        h = _axis_h(x, axis)
        result = _collapse_axis_trap(result, h, axis)

    return float(result)


# ======================================================
# SIMPSON 1/3
# ======================================================


def _simp_1_3(x, y):
    # ----------------------
    # 1D
    # ----------------------
    if not _is_nd(y):
        n = len(x) - 1
        if n % 2 != 0:
            raise ExecutionError("Simpson 1/3 requiere un numero par de subintervalos.")

        h = (x[-1] - x[0]) / n
        odd = y[1:n:2].sum()
        even = y[2 : n - 1 : 2].sum()

        return h / 3 * (y[0] + y[-1] + 4 * odd + 2 * even)

    # ----------------------
    # ND
    # ----------------------
    result = y.copy()
    for axis in reversed(range(y.ndim)):
        h = _axis_h(x, axis)
        result = _collapse_axis_simpson(result, h, axis)

    return float(result)


# ======================================================
# SIMPSON 3/8
# ======================================================


def _simp_3_8(x, y):
    # ----------------------
    # 1D
    # ----------------------
    if not _is_nd(y):
        n = len(x) - 1
        if n % 3 != 0:
            raise ExecutionError("Simpson 3/8 requiere subintervalos multiplo de 3.")

        h = (x[-1] - x[0]) / n
        sum_3 = y[3:n:3].sum()
        sum_not_3 = y[1:n].sum() - sum_3

        return 3 * h / 8 * (y[0] + y[-1] + 3 * sum_not_3 + 2 * sum_3)

    # ----------------------
    # ND
    # ----------------------
    result = y.copy()
    for axis in reversed(range(y.ndim)):
        h = _axis_h(x, axis)
        result = _collapse_axis_simpson_38(result, h, axis)

    return float(result)
