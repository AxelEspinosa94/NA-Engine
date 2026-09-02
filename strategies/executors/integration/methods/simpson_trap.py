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


# -------------------------
# Individual rule handlers
# -------------------------


def _trap_simple(x, y):
    n = len(x) - 1
    h = (x[-1] - x[0]) / n
    return h * (y[0] + y[-1]) / 2


def _trap_composite(x, y):
    n = len(x) - 1
    h = (x[-1] - x[0]) / n
    return h * (0.5 * y[0] + y[1:-1].sum() + 0.5 * y[-1])


def _simp_1_3(x, y):
    n = len(x) - 1
    h = (x[-1] - x[0]) / n
    odd = y[1:n:2].sum()
    even = y[2:n-1:2].sum()
    return h / 3 * (y[0] + y[-1] + 4 * odd + 2 * even)


def _simp_3_8(x, y):
    n = len(x) - 1
    h = (x[-1] - x[0]) / n
    sum_3 = y[3:n:3].sum()
    sum_not_3 = y[1:n].sum() - sum_3
    return 3 * h / 8 * (y[0] + y[-1] + 3 * sum_not_3 + 2 * sum_3)
