# app/callbacks/docs/components.py


def load_methods(module: str):
    if module is None:
        return []

    mapping = {
        "numerical_derivative": [
            {"label": "Forward", "value": "forward-derivative"},
            {"label": "Backward", "value": "backward-derivative"},
            {"label": "Central", "value": "central-derivative"},
            {"label": "Richardson", "value": "richardson"},
            {"label": "Partial Derivatives", "value": "partial-derivatives"},
            {"label": "Second Derivative", "value": "second-derivative"},
            {"label": "Third Derivative", "value": "third-derivative"},
        ],
        "integration": [
            {"label": "Trapezoid", "value": "trapezoid"},
            {"label": "Simpson", "value": "simpson"},
            {"label": "Romberg", "value": "romberg"},
            {"label": "Gauss-Legendre", "value": "gauss-legendre"},
            {"label": "Clenshaw-Curtis", "value": "clenshaw-curtis"},
        ],
        "interpolation": [
            {"label": "Lagrange", "value": "lagrange"},
            {"label": "Newton", "value": "newton"},
            {"label": "Hermite", "value": "hermite"},
            {"label": "Splines", "value": "spline_cubic"},
        ],
        "linear_algebra": [
            {"label": "Determinant", "value": "determinant"},
            {"label": "Inverse", "value": "inverse"},
            {"label": "Norm", "value": "norm"},
            {"label": "Condition Number", "value": "condition-number"},
            {"label": "Transpose", "value": "transpose"},
            {"label": "Rank", "value": "rank"},
            {"label": "Gauss", "value": "gauss"},
            {"label": "Gauss-Jordan", "value": "gauss-jordan"},
            {"label": "LU", "value": "lu"},
            {"label": "Cholesky", "value": "cholesky"},
            {"label": "QR", "value": "qr"},
            {"label": "Jacobi", "value": "jacobi"},
            {"label": "Gauss-Seidel", "value": "gauss-seidel"},
        ],
        "nonlinear": [
            {"label": "Bisection", "value": "bisection"},
            {"label": "Regula Falsi", "value": "false_position"},
            {"label": "Newton-Raphson", "value": "newton-raphson"},
            {"label": "Secant", "value": "secant"},
            {"label": "Fixed Point", "value": "fixed_point"},
        ],
        "ode": [
            {"label": "Euler", "value": "euler"},
            {"label": "Heun", "value": "heun"},
            {"label": "RK2", "value": "rk2"},
            {"label": "RK4", "value": "rk4"},
            {"label": "RK4 Sistema", "value": "rk4-system"},
            {"label": "Shooting", "value": "shooting"},
            {"label": "Diferencias Finitas", "value": "finite-differences-bvp"},
            {"label": "Adams–Bashforth", "value": "adams-bashforth"},
            {"label": "Adams–Moulton 2", "value": "adams-moulton-2"},
        ],
    }

    return mapping.get(module, [])
