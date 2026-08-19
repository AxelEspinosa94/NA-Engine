from core.exceptions import ValidationError

def _validate_gauss_points(input_data):
    n = input_data.get("n")
    gp = input_data.get("gauss_points", 2)
    if gp > 50:
        raise ValidationError("Gauss-Legendre unstable for n > 50.")
    if not isinstance(gp, int) or gp <= 0:
        raise ValidationError("Gauss-Legendre requires positive integer gauss_points.")