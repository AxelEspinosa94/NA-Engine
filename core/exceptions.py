# core/exceptions.py

class CatalogLoadError(Exception):
    pass


class MethodNotFoundError(Exception):
    pass


class ValidationError(Exception):
    pass


class ExecutionError(Exception):
    pass
