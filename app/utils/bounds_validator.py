from core.exceptions import ConstructionError


def validate_bounds(bounds):

    if not isinstance(bounds, (list, tuple)):
        raise ConstructionError("Bounds must be a list.")

    if len(bounds) == 0:
        raise ConstructionError("Bounds cannot be empty.")

    if not isinstance(bounds[0], (list, tuple)):
        bounds = [bounds]

    for interval in bounds:

        if not isinstance(interval, (list, tuple)):
            raise ConstructionError("Each bound must be a list or tuple.")

        if len(interval) != 2:
            raise ConstructionError(
                f"Invalid interval: {interval}. "
                "Each bound must contain exactly two values."
            )

        a, b = interval

        if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
            raise ConstructionError(f"Invalid interval: {interval}.")

        if a >= b:
            raise ConstructionError(f"Invalid interval [{a}, {b}].")
    return bounds
