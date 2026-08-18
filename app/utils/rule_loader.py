import importlib

def load_rule(path: str):
    """
    path example:
    validators.integration.rules.clenshaw_rules.validate_n
    """
    module_path, func_name = path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, func_name)
