import time

import pytest

from app.utils.build_function import build_function
from core.base_method import NumericalMethod

# Métodos soportados
METHODS = [
    "trapezoid_simple",
    "trapezoid_composite",
    "simpson_1_3",
    "simpson_3_8",
    "romberg",
    "gauss",
    "clenshaw_curtis",
    "montecarlo",
]

# Tamaños grandes para medir performance
N_PERF = {
    "trapezoid_simple": 1,
    "trapezoid_composite": 5000,
    "simpson_1_3": 5000,
    "simpson_3_8": 6000,  # múltiplo de 3
    "romberg": 10,  # romberg explota con n grande
    "gauss": 40,  # gauss estable
    "clenshaw_curtis": 1000,  # CC es O(N log N)
    "montecarlo": 10000,  # MC es O(N)
}

# Límites de tiempo razonables por método (segundos)
LIMITS = {
    "trapezoid_simple": 0.50,
    "trapezoid_composite": 1.0,
    "simpson_1_3": 0.50,
    "simpson_3_8": 0.50,
    "romberg": 1.0,
    "gauss": 1.0,
    "clenshaw_curtis": 1.0,  # CC es O(N log N)
    "montecarlo": 3.50,  # MC puede ser lento
}


def make_outcome(method: str, function: str, interval: list, n: int):
    input_data = {
        "mode": "function",
        "function": function,
        "bounds": interval,
        "n": n,
        "calculation_mode": method,
    }
    if method == "gauss":
        input_data["gauss_points"] = (
            n  # for Gauss, n is irrelevant, but we need to set gauss_points
        )
    nm = NumericalMethod(
        method="integration",
        input_data=input_data,
    )
    nm.validate_input()
    t0 = time.perf_counter()
    outcome = nm.execute()
    elapsed = time.perf_counter() - t0
    return outcome, elapsed


# ────────────────────────────────────────────────────────────────
# PERFORMANCE: tiempo de ejecución
# ────────────────────────────────────────────────────────────────


@pytest.fixture(scope="session", autouse=True)
def warmup_sympy():
    build_function("sin(x) + exp(x)", ["x"])


@pytest.mark.parametrize("method", METHODS)
def test_performance(method):
    """
    Cada método debe ejecutarse por debajo de un límite razonable.
    No se verifica exactitud, solo tiempo y estabilidad.
    """
    n = N_PERF[method]
    limit = LIMITS[method]

    outcome, elapsed = make_outcome(method, "sin(x)", [0, 10], n)

    assert outcome["status"] == "success"
    assert elapsed < limit, f"{method} tardó {elapsed:.4f}s (límite {limit}s)"


# ────────────────────────────────────────────────────────────────
# PERFORMANCE: determinismo temporal
# ────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("method", METHODS)
def test_performance_determinismo(method):
    """
    Dos ejecuciones consecutivas deben tener tiempos similares.
    No exactos, pero no deben diferir por órdenes de magnitud.
    """
    n = N_PERF[method]

    t1_start = time.perf_counter()
    make_outcome(method, "sin(x)", [0, 10], n)
    t1 = time.perf_counter() - t1_start

    t2_start = time.perf_counter()
    make_outcome(method, "sin(x)", [0, 10], n)
    t2 = time.perf_counter() - t2_start

    ratio = max(t1, t2) / min(t1, t2)

    # Aceptamos hasta 2x de variación por ruido del sistema
    assert ratio < 2.0, f"Variación temporal excesiva: {ratio:.2f}x"


# ────────────────────────────────────────────────────────────────
# PERFORMANCE: intervalos grandes
# ────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("method", METHODS)
def test_performance_intervalo_grande(method):
    """
    Intervalos grandes no deben afectar el tiempo de ejecución significativamente.
    """
    n = N_PERF[method]
    limit = LIMITS[method] * 2  # un poco más permisivo

    outcome, elapsed = make_outcome(method, "exp(x)", [-100, 100], n)

    assert outcome["status"] == "success"
    assert elapsed < limit, f"{method} tardó {elapsed:.4f}s en intervalo grande"
