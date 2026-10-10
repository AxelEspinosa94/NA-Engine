from core.exceptions import ConstructionError


def _build_nd_domain(bounds):
    if not isinstance(bounds, (list, tuple)):
        raise ConstructionError("ND mode requires bounds list.")

    for interval in bounds:
        if len(interval) != 2:
            raise ConstructionError("Each bound must be [a, b].")
        a, b = interval
        if a >= b:
            raise ConstructionError("Each interval must satisfy a < b.")
