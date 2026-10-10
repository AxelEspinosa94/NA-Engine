# tests/unit/core/integration/test_integral_constructor.py

from core.integration.integral import Integral

# ============================================================================
# ROMBERG 1D
# ============================================================================


def test_romberg_1d_constructor():
    integral = Integral(
        {
            "mode": "function",
            "calculation_mode": "romberg",
            "function": "x**2",
            "bounds": [0, 1],
            "n": 10,
        }
    )

    assert integral.mode == "function"
    assert integral.dim == 1

    assert len(integral.x) == 11
    assert len(integral.y) == 11


# ============================================================================
# ROMBERG ND
# ============================================================================


def test_romberg_nd_constructor():
    integral = Integral(
        {
            "mode": "function",
            "calculation_mode": "romberg",
            "function": "x0**2 + x1",
            "bounds": [[0, 1], [2, 4]],
            "n": 10,
        }
    )

    assert integral.dim == 2

    grids = integral.x

    assert len(grids) == 2

    assert grids[0].shape == (11, 11)
    assert grids[1].shape == (11, 11)

    assert integral.y.shape == (11, 11)


# ============================================================================
# MONTECARLO 1D
# ============================================================================


def test_montecarlo_1d_constructor():
    integral = Integral(
        {
            "mode": "function",
            "calculation_mode": "montecarlo",
            "function": "x**2",
            "bounds": [0, 1],
            "n": 100,
        }
    )

    assert integral.dim == 1

    assert integral.x.shape == (100, 1)
    assert integral.y.shape == (100,)

    assert integral.y.dtype.kind in {"f", "i"}


# ============================================================================
# MONTECARLO 2D
# ============================================================================


def test_montecarlo_nd_constructor():
    integral = Integral(
        {
            "mode": "function",
            "calculation_mode": "montecarlo",
            "function": "x0**2 + x1",
            "bounds": [[0, 1], [2, 4]],
            "n": 100,
        }
    )

    assert integral.dim == 2

    assert integral.x.shape == (100, 2)
    assert integral.y.shape == (100,)

    assert integral.y.dtype.kind in {"f", "i"}


# ============================================================================
# MONTECARLO 3D
# ============================================================================


def test_montecarlo_3d_constructor():
    integral = Integral(
        {
            "mode": "function",
            "calculation_mode": "montecarlo",
            "function": "x0 + x1 + x2",
            "bounds": [
                [0, 1],
                [1, 2],
                [2, 3],
            ],
            "n": 100,
        }
    )

    assert integral.dim == 3

    assert integral.x.shape == (100, 3)
    assert integral.y.shape == (100,)


# ============================================================================
# CONSTANT FUNCTION ND
# ============================================================================


def test_constant_function_nd():
    integral = Integral(
        {
            "mode": "function",
            "calculation_mode": "montecarlo",
            "function": "5",
            "bounds": [[0, 1], [0, 1]],
            "n": 5,
        }
    )

    assert (integral.y == 5).all()
