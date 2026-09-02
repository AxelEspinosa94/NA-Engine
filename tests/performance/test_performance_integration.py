import time

import pytest

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
]

# Tamaños grandes para medir performance
N_PERF = {
    "trapezoid_simple": 1,
    "trapezoid_composite": 5000,
    "simpson_1_3": 5000,
    "simpson_3_8": 6000,  # múltiplo de 3
    "romberg": 10,  # romberg explota con n grande
    "gauss": 40,  # gauss estable
    "clenshaw_curtis": 2000,  # CC es O(N log N)
}

# Límites de tiempo razonables por método (segundos)
LIMITS = {
    "trapezoid_simple": 2,
    "trapezoid_composite": 0.20,
    "simpson_1_3": 0.25,
    "simpson_3_8": 0.30,
    "romberg": 0.10,
    "gauss": 0.15,
    "clenshaw_curtis": 0.30,
}


def make_outcome(method: str, function: str, interval: list, n: int):
    nm = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": function,
            "interval": interval,
            "n": n,
            "calculation_mode": method,
        },
    )
    nm.validate_input()
    return nm.execute()


# ────────────────────────────────────────────────────────────────
# PERFORMANCE: tiempo de ejecución
# ────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("method", METHODS)
def test_performance(method):
    """
    Cada método debe ejecutarse por debajo de un límite razonable.
    No se verifica exactitud, solo tiempo y estabilidad.
    """
    n = N_PERF[method]
    limit = LIMITS[method]

    start = time.perf_counter()
    outcome = make_outcome(method, "sin(x)", [0, 10], n)
    elapsed = time.perf_counter() - start

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

    start = time.perf_counter()
    outcome = make_outcome(method, "exp(x)", [-100, 100], n)
    elapsed = time.perf_counter() - start

    assert outcome["status"] == "success"
    assert elapsed < limit, f"{method} tardó {elapsed:.4f}s en intervalo grande"
