import pytest

from core.base_method import NumericalMethod
from core.exceptions import ConstructionError

# ============================================================
# HELPERS
# ============================================================

K_SIGMA = 5  # tolerancia en errores estandar
DEFAULT_SEED = 12345


def build_mc(function, bounds, n, seed=DEFAULT_SEED):
    """Construye el metodo sin ejecutarlo (util para tests de validacion)."""
    input_data = {
        "mode": "function",
        "function": function,
        "bounds": bounds,
        "n": n,
        "calculation_mode": "montecarlo",
    }
    if seed is not None:
        input_data["seed"] = seed

    return NumericalMethod(method="integration", input_data=input_data)


def run_mc(function, bounds, n, seed=DEFAULT_SEED):
    """Construye, ejecuta y devuelve el dict 'result' del metodo."""
    return build_mc(function, bounds, n, seed).execute().get("result", {})


def assert_mc_close(result, exact, k=K_SIGMA):
    """
    |estimado - exacto| <= k * std_error.
    El 1e-12 cubre el caso std_error == 0 (funcion constante).
    """
    assert abs(result["value"] - exact) <= k * result["std_error"] + 1e-12


# ============================================================
# EXACTITUD (semilla fija -> deterministas)
# ============================================================


@pytest.mark.parametrize(
    "function, bounds, n, exact",
    [
        # 1D
        ("x**2", [0, 1], 10_000, 1 / 3),
        ("5", [0, 1], 1_000, 5.0),
        ("x", [0, 1], 12_000, 0.5),
        # volumen distinto de 1: detecta errores en el factor del volumen
        ("x", [0, 4], 20_000, 8.0),
        ("x**2", [-1, 1], 20_000, 2 / 3),
        # 2D
        ("x0 + x1", [[0, 1], [0, 1]], 10_000, 1.0),
        ("x0 * x1", [[0, 2], [0, 3]], 20_000, 9.0),
        # 3D
        ("x0 + x1 + x2", [[0, 1]] * 3, 1_000, 1.5),
    ],
)
def test_montecarlo_matches_analytic(function, bounds, n, exact):
    assert_mc_close(run_mc(function, bounds, n), exact)


# ============================================================
# PROPIEDADES DEL ESTIMADOR
# ============================================================


def test_reproducible_with_same_seed():
    a = run_mc("x**2", [0, 1], 5_000, seed=7)["value"]
    b = run_mc("x**2", [0, 1], 5_000, seed=7)["value"]
    assert a == b


def test_different_seeds_differ():
    a = run_mc("x**2", [0, 1], 5_000, seed=1)["value"]
    b = run_mc("x**2", [0, 1], 5_000, seed=2)["value"]
    assert a != b


def test_constant_function_has_zero_std_error():
    result = run_mc("5", [0, 1], 1_000)
    assert result["std_error"] == pytest.approx(0.0, abs=1e-12)


def test_std_error_scales_as_inverse_sqrt_n():
    # n x100 -> error estandar ~ /10
    se_small = run_mc("x**2", [0, 1], 1_000)["std_error"]
    se_big = run_mc("x**2", [0, 1], 100_000)["std_error"]
    assert 7 < se_small / se_big < 14


def test_std_error_scales_with_volume():
    # mismo integrando normalizado, dominio 4x mas largo -> se x4
    se_unit = run_mc("x", [0, 1], 20_000, seed=3)["std_error"]
    se_long = run_mc("x", [0, 4], 20_000, seed=3)["std_error"]
    assert se_long / se_unit == pytest.approx(16.0, rel=0.05)


@pytest.mark.slow
def test_confidence_interval_coverage():
    # ~95% de los intervalos de 1.96 * se deben contener el valor real
    exact, reps, hits = 1 / 3, 300, 0
    for seed in range(reps):
        r = run_mc("x**2", [0, 1], 2_000, seed=seed)
        hits += abs(r["value"] - exact) <= 1.96 * r["std_error"]
    assert 0.90 < hits / reps < 0.99


# ============================================================
# VALIDACIONES
# ============================================================


def test_montecarlo_rejects_empty_function():
    with pytest.raises(ConstructionError):
        build_mc("", [0, 1], 10)


def test_montecarlo_rejects_empty_bounds():
    with pytest.raises(ConstructionError):
        build_mc("x", [], 10)


def test_montecarlo_rejects_invalid_interval_length():
    with pytest.raises(ConstructionError):
        build_mc("x0+x1", [[0, 1], [2], [3, 4]], 10)


def test_montecarlo_rejects_reversed_interval():
    with pytest.raises(ConstructionError):
        build_mc("x", [1, 0], 10)


def test_montecarlo_rejects_non_positive_n():
    with pytest.raises(ConstructionError):
        build_mc("x", [0, 1], 0)
