from core.base_method import NumericalMethod

# ============================================================
# TRAPECIO ND
# ============================================================


def test_trapezoid_nd_linear():
    """
    ∫∫ (x0 + x1) sobre [0,1]² = 1
    """

    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "x0 + x1",
            "bounds": [[0, 1], [0, 1]],
            "n": 20,
            "calculation_mode": "trapezoid_composite",
        },
    )

    result = method.execute()["result"]

    assert abs(result["value"] - 1.0) < 1e-2


# ============================================================
# SIMPSON 1/3 ND
# ============================================================


def test_simpson_1_3_nd_linear():
    """
    ∫∫ (x0 + x1) sobre [0,1]² = 1
    """

    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "x0 + x1",
            "bounds": [[0, 1], [0, 1]],
            "n": 10,
            "calculation_mode": "simpson_1_3",
        },
    )

    result = method.execute()["result"]

    assert abs(result["value"] - 1.0) < 1e-10


# ============================================================
# SIMPSON 3/8 ND
# ============================================================


def test_simpson_3_8_nd_linear():
    """
    ∫∫ (x0 + x1) sobre [0,1]² = 1
    """

    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "x0 + x1",
            "bounds": [[0, 1], [0, 1]],
            "n": 12,
            "calculation_mode": "simpson_3_8",
        },
    )

    result = method.execute()["result"]

    assert abs(result["value"] - 1.0) < 1e-10


# ============================================================
# ROMBERG ND
# ============================================================


def test_romberg_nd_linear():
    """
    ∫∫ (x0 + x1) sobre [0,1]² = 1
    """

    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "x0 + x1",
            "bounds": [[0, 1], [0, 1]],
            "n": 5,
            "calculation_mode": "romberg",
        },
    )

    result = method.execute()["result"]

    assert abs(result["value"] - 1.0) < 1e-10


# ============================================================
# GAUSS LEGENDRE ND
# ============================================================


def test_gauss_legendre_nd_quadratic():
    """
    ∫∫ (x0² + x1²) sobre [0,1]² = 2/3
    """

    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "x0**2 + x1**2",
            "bounds": [[0, 1], [0, 1]],
            "n": 4,
            "gauss_points": 5,
            "calculation_mode": "gauss",
        },
    )

    result = method.execute()["result"]

    assert abs(result["value"] - 2 / 3) < 1e-12


# ============================================================
# CLENSHAW CURTIS ND
# ============================================================


def test_clenshaw_nd_linear():
    """
    ∫∫ (x0 + x1) sobre [0,1]² = 1
    """

    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "x0 + x1",
            "bounds": [[0, 1], [0, 1]],
            "n": 20,
            "calculation_mode": "clenshaw_curtis",
        },
    )

    result = method.execute()["result"]

    assert abs(result["value"] - 1.0) < 1e-4


# ============================================================
# 3D TEST
# ============================================================


def test_simpson_1_3_3d_linear():
    """
    ∭ (x0 + x1 + x2) sobre [0,1]³ = 3/2
    """

    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "x0 + x1 + x2",
            "bounds": [
                [0, 1],
                [0, 1],
                [0, 1],
            ],
            "n": 10,
            "calculation_mode": "simpson_1_3",
        },
    )

    result = method.execute()["result"]

    assert abs(result["value"] - 1.5) < 1e-10


# ============================================================
# CONSTANT FUNCTION ND
# ============================================================


def test_constant_nd():
    """
    ∫∫ 5 dA sobre [0,1]² = 5
    """

    method = NumericalMethod(
        method="integration",
        input_data={
            "mode": "function",
            "function": "5",
            "bounds": [[0, 1], [0, 1]],
            "n": 10,
            "calculation_mode": "romberg",
        },
    )

    result = method.execute()["result"]

    assert abs(result["value"] - 5.0) < 1e-10
