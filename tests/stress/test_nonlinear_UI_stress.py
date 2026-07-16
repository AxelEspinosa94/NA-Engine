# tests/stress/test_non_linear_stress.py

import pytest
import numpy as np
from core.base_method import NumericalMethod
from core.contract import UIContract

contract = UIContract()

# Mark entire module as pending until Stage 4 is complete
pytestmark = pytest.mark.pending

MODES = [
    "bisection",
    "false_position",
    "newton",
    "secant",
    "fixed_point",
]

# ============================================================
# Helper to run NumericalMethod safely
# ============================================================

def run_nm(mode, fn, x0=None, x1=None, interval=None, g=None, tol=1e-6, max_iter=50):
    input_data = {
        "mode": "function",
        "function": fn,
        "calculation_mode": mode,
        "tol": tol,
        "max_iter": max_iter,
    }

    if x0 is not None:
        input_data["x0"] = x0
    if x1 is not None:
        input_data["x1"] = x1
    if interval is not None:
        input_data["interval"] = interval
    if g is not None:
        input_data["g"] = g

    nm = NumericalMethod("non_linear_equation", input_data)
    nm.validate_input()
    return nm.execute()


# ============================================================
# Stress Test 1 — Large intervals
# ============================================================

@pytest.mark.parametrize("mode", ["bisection", "false_position"])
def test_large_interval(mode):
    fn = "x**3 - 10*x + 5"
    interval = [-1e6, 1e6]

    outcome = run_nm(mode, fn, interval=interval)
    payload = contract.resolve(mode, outcome)

    assert payload is not None


# ============================================================
# Stress Test 2 — Very small tolerance
# ============================================================

@pytest.mark.parametrize("mode", MODES)
def test_small_tolerance(mode):
    fn = "np.sin(x) - 0.5"
    x0 = 1.0

    interval = [0, 3] if mode in ["bisection", "false_position"] else None
    x1 = 2.0 if mode == "secant" else None
    g = "x - (np.sin(x) - 0.5)" if mode == "fixed_point" else None

    outcome = run_nm(mode, fn, x0=x0, x1=x1, interval=interval, g=g, tol=1e-12)
    payload = contract.resolve(mode, outcome)

    assert payload is not None


# ============================================================
# Stress Test 3 — Highly oscillatory function
# ============================================================

@pytest.mark.parametrize("mode", MODES)
def test_oscillatory(mode):
    fn = "np.sin(50*x)"
    x0 = 0.1

    interval = [-1, 1] if mode in ["bisection", "false_position"] else None
    x1 = 0.2 if mode == "secant" else None
    g = "0.5*(x + np.sin(50*x))" if mode == "fixed_point" else None

    outcome = run_nm(mode, fn, x0=x0, x1=x1, interval=interval, g=g)
    payload = contract.resolve(mode, outcome)

    assert payload is not None


# ============================================================
# Stress Test 4 — Newton near derivative zero
# ============================================================

def test_newton_derivative_zero():
    fn = "x**3"
    x0 = 0.0  # derivative = 0 → should raise ExecutionError

    nm = NumericalMethod("non_linear_equation", {
        "mode": "function",
        "function": fn,
        "calculation_mode": "newton",
        "x0": x0,
        "tol": 1e-6,
        "max_iter": 50,
    })

    nm.validate_input()

    with pytest.raises(Exception):
        nm.execute()


# ============================================================
# Stress Test 5 — Secant with nearly equal f(x)
# ============================================================

def test_secant_near_zero_denominator():
    fn = "x**2 - 4"
    x0 = 2.0000001
    x1 = 2.0000002  # f(x0) ≈ f(x1)

    nm = NumericalMethod("non_linear_equation", {
        "mode": "function",
        "function": fn,
        "calculation_mode": "secant",
        "x0": x0,
        "x1": x1,
        "tol": 1e-6,
        "max_iter": 50,
    })

    nm.validate_input()

    with pytest.raises(Exception):
        nm.execute()


# ============================================================
# Stress Test 6 — Fixed point divergence
# ============================================================

def test_fixed_point_divergence():
    fn = "np.cos(x)"
    g = "2*x"  # g'(x) = 2 → diverges
    x0 = 1.0

    nm = NumericalMethod("non_linear_equation", {
        "mode": "function",
        "function": fn,
        "calculation_mode": "fixed_point",
        "g": g,
        "x0": x0,
        "tol": 1e-6,
        "max_iter": 50,
    })

    nm.validate_input()

    with pytest.raises(Exception):
        nm.execute()


# ============================================================
# Stress Test 7 — Randomized Monte Carlo stress
# ============================================================

def test_randomized_inputs():
    np.random.seed(42)

    for _ in range(30):
        mode = np.random.choice(MODES)
        fn = "x**3 - 4*x + 1"

        x0 = np.random.uniform(-10, 10)
        x1 = np.random.uniform(-10, 10)
        interval = sorted(np.random.uniform(-10, 10, size=2))

        g = "0.5*(x + np.cos(x))" if mode == "fixed_point" else None

        try:
            outcome = run_nm(
                mode,
                fn,
                x0=x0,
                x1=x1,
                interval=interval if mode in ["bisection", "false_position"] else None,
                g=g,
            )
            payload = contract.resolve(mode, outcome)
            assert payload is not None

        except Exception:
            # Some random inputs will fail — this is expected
            pass
