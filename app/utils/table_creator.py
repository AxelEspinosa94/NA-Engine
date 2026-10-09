import importlib

from core.exceptions import ConstructionError


def _import_creator(name: str):
    """
    Dynamically import a creator function.
    Accepts 'module.func' or 'func' (assumes creators module).
    """
    if "." in name:
        module_name, func_name = name.rsplit(".", 1)
    else:
        module_name = "integrators.creators"  # adjust to your package
        func_name = name

    try:
        mod = importlib.import_module(module_name)
        func = getattr(mod, func_name)
        return func
    except Exception as e:
        raise ConstructionError(f"Could not import tb_creator '{name}': {e}")
