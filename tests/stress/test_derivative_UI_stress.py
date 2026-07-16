# tests/stress/test_derivative_stress.py

import pytest
import numpy as np
from core.base_method import NumericalMethod
from core.contract import UIContract

contract = UIContract()

# Mark entire module as pending until Stage 4 is complete
#pytestmark = pytest.mark.pending


MODES = [
    "forward",
    "backward",
    "central",
    "richardson",
    "second_forward",
    "second_central",
    "third_forward",
    "partial_x",
    "partial_y",
]

# ============================================================
# Helper: build NumericalMethod safely
# ============================================================

def run_nm(mode, fn, x, h, y=None, richardson_order=None):
    input_data = {
        "function": fn,
        "x": float(x),
        "h": float(h),
        "calculation_mode": mode,
    }

    if y is not None:
        input_data["y"] = float(y)

    if richardson_order is not None:
        input_data["richardson_order"] = int(richardson_order)

    nm = NumericalMethod("numerical_derivative", input_data)
    nm.validate_input()
    return nm.execute()


# ============================================================
# Stress Test 1 — Large x values
# ============================================================

@pytest.mark.parametrize("mode", MODES)
def test_large_x(mode):
    fn = "x**3 - 4*x + 10"
    x = 1e6
    h = 1e-3

    y = 2.0 if mode in ["partial_x", "partial_y"] else None

    outcome = run_nm(mode, fn, x, h, y)
    payload = contract.resolve(mode, outcome)

    assert payload is not None


# ============================================================
# Stress Test 2 — Very small h (precision stress)
# ============================================================

@pytest.mark.parametrize("mode", MODES)
def test_small_h(mode):
    fn = "sin(x) + x**2"
    x = 2.0
    h = 1e-10

    y = 1.0 if mode in ["partial_x", "partial_y"] else None

    outcome = run_nm(mode, fn, x, h, y)
    payload = contract.resolve(mode, outcome)

    assert payload is not None


# ============================================================
# Stress Test 3 — Very large h (instability stress)
# ============================================================

@pytest.mark.parametrize("mode", MODES)
def test_large_h(mode):
    fn = "np.exp(x) - np.log(x)"
    x = 5.0
    h = 50.0

    y = 3.0 if mode in ["partial_x", "partial_y"] else None

    outcome = run_nm(mode, fn, x, h, y)
    payload = contract.resolve(mode, outcome)

    assert payload is not None


# ============================================================
# Stress Test 4 — Highly oscillatory function
# ============================================================

@pytest.mark.parametrize("mode", MODES)
def test_oscillatory(mode):
    fn = "np.sin(100*x)"
    x = 0.1
    h = 1e-3

    y = 0.5 if mode in ["partial_x", "partial_y"] else None

    outcome = run_nm(mode, fn, x, h, y)
    payload = contract.resolve(mode, outcome)

    assert payload is not None


# ============================================================
# Stress Test 5 — Partial derivatives with mixed variables
# ============================================================

@pytest.mark.parametrize("mode", ["partial_x", "partial_y"])
def test_partial_mixed(mode):
    fn = "x*y + np.sin(x*y) + y**3"
    x = 2.0
    y = 3.0
    h = 1e-2

    outcome = run_nm(mode, fn, x, h, y)
    payload = contract.resolve(mode, outcome)

    assert payload is not None


# ============================================================
# Stress Test 6 — Richardson with high order
# ============================================================

@pytest.mark.parametrize("p", [2, 4, 6, 8])
def test_richardson_high_order(p):
    fn = "np.cos(x)"
    x = 1.0
    h = 1e-3

    outcome = run_nm("richardson", fn, x, h, None, richardson_order=p)
    payload = contract.resolve("richardson", outcome)

    assert payload is not None


# ============================================================
# Stress Test 7 — Randomized inputs (Monte Carlo stress)
# ============================================================

def test_randomized_inputs():
    np.random.seed(42)

    for _ in range(50):
        mode = np.random.choice(MODES)
        x = np.random.uniform(-100, 100)
        h = np.random.uniform(1e-6, 1e2)
        y = np.random.uniform(-50, 50) if mode in ["partial_x", "partial_y"] else None

        fn = "np.sin(x) + x**3 - 4*x + 10"

        outcome = run_nm(mode, fn, x, h, y)
        payload = contract.resolve(mode, outcome)

        assert payload is not None
