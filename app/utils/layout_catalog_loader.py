import importlib

def load_component(path):
    """
    path: "layout.integration.components.integr_method.integr_method"
    """
    module_path, attr = path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, attr)
