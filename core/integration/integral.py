import os

from app.utils.bounds_validator import validate_bounds
from app.utils.build_function import build_function
from app.utils.catalog_loader import load_catalog
from app.utils.check_function import check_function_dims
from app.utils.table_creator import _import_creator
from core.exceptions import ConstructionError


class Integral:
    """
    Base class for all integration methods.
    Only supports mode='function'.
    """

    def __init__(self, input_data):
        base = os.path.dirname(__file__)
        path = os.path.join(base, "integration_constructor_catalog.json")
        self.catalog = load_catalog(path)

        self.input_data = input_data
        self.mode = self.input_data.get("mode")
        self.calculation_mode = self.input_data.get("calculation_mode")

        if self.mode != "function":
            raise ConstructionError("Integration only supports mode='function'.")

        # Build function
        if not self.input_data.get("function"):
            raise ConstructionError("Function expression is required.")

        self.func_str = self.input_data.get("function")

        # Domain type (from catalog)
        self.domain = self.catalog.get(self.calculation_mode, {}).get(
            "domain"
        )  # "1d" or "nd"

        bounds = self.input_data.get("bounds")

        self.bounds = validate_bounds(bounds)

        # n
        self.n = self.input_data.get("n")
        if not isinstance(self.n, int) or self.n <= 0:
            raise ConstructionError("n must be a positive integer.")

        self.dim = len(self.bounds)
        check_result = check_function_dims(self.func_str, self.dim)
        if check_result:
            raise ConstructionError(check_result)

        # Build function with appropriate symbols: x y z ...
        if self.dim == 1:
            self.symbols = ["x"]
        else:
            self.symbols = [f"x{i}" for i in range(self.dim)]

        self.f = build_function(self.func_str, self.symbols)

        tb_creator_name = self.catalog.get(self.calculation_mode, {}).get(
            "tb_creator", None
        )
        if tb_creator_name:
            # tb_creator may be "module.func" or just "func" in a known module
            self.creator = _import_creator(tb_creator_name)
            self.x, self.y = (
                self.creator(self.func_str, self.symbols, self.bounds, self.n)
                if self.creator
                else None
            )
        else:
            self.creator = None
            self.x = None
            self.y = None

        if (
            self.calculation_mode == "gauss"
            and self.input_data.get("gauss_points", None) is None
        ):
            raise ConstructionError(
                "gauss_points must be provided for gauss calculation mode."
            )
        elif (
            self.calculation_mode != "gauss"
            and self.input_data.get("gauss_points", None) is not None
        ):
            raise ConstructionError("Too many arguments provided")
