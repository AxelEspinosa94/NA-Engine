# tests/stress/test_ode_stress.py

import pytest
import numpy as np
from core.base_method import NumericalMethod
from core.contract import UIContract

contract = UIContract()

# Mark entire module as pending until Stage 4 is complete
pytestmark = pytest.mark.pending

IVP_MODES = [
    "euler",
    "heun",
    "rk2",
    "rk4",
    "adams_bashforth_2",
    "adams_bashforth_3",
    "adams_moulton_2",
]

# ═══════════════════════════════════════════════════════════════
# 1. LARGE INTERVALS — stability under huge domains
# ═══════════════════════════════════════════════════════════════

@pytest.mark.parametrize("mode", IVP_MODES)
def test_large_interval(mode):
    nm = NumericalMethod("ode", {
        "function": "x + y",
        "x0": 0.0,
        "y0": 1.0,
        "x_end": 500.0,   # huge domain
        "h": 0.5,
        "calculation_mode": mode,
    })

    nm.validate_input()
    outcome = nm.execute()
    payload = contract.resolve(mode, outcome)

    assert payload is not None


# ═══════════════════════════════════════════════════════════════
# 2. VERY SMALL h — precision stress
# ═══════════════════════════════════════════════════════════════

@pytest.mark.parametrize("mode", IVP_MODES)
def test_small_h(mode):
    nm = NumericalMethod("ode", {
        "function": "np.sin(x) + y",
        "x0": 0.0,
        "y0": 1.0,
        "x_end": 1.0,
        "h": 1e-6,        # extremely small step
        "calculation_mode": mode,
    })

    nm.validate_input()
    outcome = nm.execute()
    payload = contract.resolve(mode, outcome)

    assert payload is not None


# ═══════════════════════════════════════════════════════════════
# 3. VERY LARGE h — instability stress
# ═══════════════════════════════════════════════════════════════

@pytest.mark.parametrize("mode", IVP_MODES)
def test_large_h(mode):
    nm = NumericalMethod("ode", {
        "function": "np.exp(x) - y",
        "x0": 0.0,
        "y0": 1.0,
        "x_end": 10.0,
        "h": 5.0,         # huge step
        "calculation_mode": mode,
    })

    nm.validate_input()
    outcome = nm.execute()
    payload = contract.resolve(mode, outcome)

    assert payload is not None


# ═══════════════════════════════════════════════════════════════
# 4. OSCILLATORY FUNCTIONS — stability under high frequency
# ═══════════════════════════════════════════════════════════════

@pytest.mark.parametrize("mode", IVP_MODES)
def test_oscillatory(mode):
    nm = NumericalMethod("ode", {
        "function": "np.sin(100*x) + y",
        "x0": 0.0,
        "y0": 0.0,
        "x_end": 2.0,
        "h": 0.01,
        "calculation_mode": mode,
    })

    nm.validate_input()
    outcome = nm.execute()
    payload = contract.resolve(mode, outcome)

    assert payload is not None


# ═══════════════════════════════════════════════════════════════
# 5. SYSTEMS — large dimensional RK4 system
# ═══════════════════════════════════════════════════════════════

def test_large_system_rk4():
    # y_i' = -y_i  → exponential decay
    n = 10
    system = ["-y{}".format(i+1) for i in range(n)]
    y0 = [1.0] * n

    nm = NumericalMethod("ode", {
        "system": system,
        "y0": y0,
        "x0": 0.0,
        "x_end": 2.0,
        "h": 0.05,
        "calculation_mode": "rk4_system",
    })

    nm.validate_input()
    outcome = nm.execute()
    payload = contract.resolve("rk4_system", outcome)

    assert payload is not None


# ═══════════════════════════════════════════════════════════════
# 6. SHOOTING — difficult BVP
# ═══════════════════════════════════════════════════════════════

def test_shooting_stress():
    nm = NumericalMethod("ode", {
        "function": "np.sin(x) + y",
        "x0": 0.0,
        "x_end": 10.0,
        "alpha": 0.0,
        "beta": 5.0,
        "s0": 1.0,
        "h": 0.1,
        "calculation_mode": "shooting",
    })

    nm.validate_input()
    outcome = nm.execute()
    payload = contract.resolve("shooting", outcome)

    assert payload is not None


# ═══════════════════════════════════════════════════════════════
# 7. FINITE DIFFERENCES — large n
# ═══════════════════════════════════════════════════════════════

def test_finite_diff_large_n():
    nm = NumericalMethod("ode", {
        "function": "np.sin(x)",
        "x0": 0.0,
        "x_end": 5.0,
        "alpha": 0.0,
        "beta": 1.0,
        "n": 200,  # large grid
        "calculation_mode": "finite_differences",
    })

    nm.validate_input()
    outcome = nm.execute()
    payload = contract.resolve("finite_differences", outcome)

    assert payload is not None


# ═══════════════════════════════════════════════════════════════
# 8. DETERMINISM — same input → same output
# ═══════════════════════════════════════════════════════════════

def test_determinism_rk4():
    input_data = {
        "function": "x + y",
        "x0": 0.0,
        "y0": 1.0,
        "x_end": 5.0,
        "h": 0.1,
        "calculation_mode": "rk4",
    }

    nm1 = NumericalMethod("ode", input_data)
    nm2 = NumericalMethod("ode", input_data)

    nm1.validate_input()
    nm2.validate_input()

    r1 = nm1.execute().get("result")
    r2 = nm2.execute().get("result")

    assert np.allclose(r1["y"], r2["y"])
