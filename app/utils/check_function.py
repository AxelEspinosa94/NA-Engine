import re


def check_function_dims(fn: str, dim: int):
    used = {int(m) for m in re.findall(r"\bx(\d+)\b", fn)}
    if not used:
        return None  # p.ej. función constante; decide si lo permites
    if max(used) >= dim:
        return f"La función usa x{max(used)} pero solo definiste {dim} dimensión(es)."
    missing = set(range(dim)) - used
    if missing:
        return (
            f"Definiste {dim} dimensiones pero la función no usa "
            + ", ".join(f"x{i}" for i in sorted(missing))
            + "."
        )
    return None
