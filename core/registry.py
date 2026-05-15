import json
import os
from typing import Dict, Any

from core.exceptions import CatalogLoadError, MethodNotFoundError


class MethodRegistry:
    """
    Loads and manages the method catalog used by NumericalMethod.
    Provides a clean interface to retrieve method metadata.
    """

    _catalog_cache: Dict[str, Any] = None  # Cache to avoid reloading JSON repeatedly

    @classmethod
    def load_catalog(cls) -> Dict[str, Any]:
        """
        Loads the method_catalog.json file.
        Uses an internal cache so the file is only read once.
        """
        if cls._catalog_cache is not None:
            return cls._catalog_cache

        catalog_path = os.path.join(
            os.path.dirname(__file__),
            "method_catalog.json"
        )

        if not os.path.exists(catalog_path):
            raise CatalogLoadError(f"Catalog file not found at: {catalog_path}")

        try:
            with open(catalog_path, "r") as f:
                cls._catalog_cache = json.load(f)
        except Exception as e:
            raise CatalogLoadError("Failed to load method catalog JSON.") from e

        return cls._catalog_cache

    @classmethod
    def get_method_info(cls, method: str) -> Dict[str, Any]:
        """
        Returns the catalog entry for a specific method.
        """
        catalog = cls.load_catalog()

        if method not in catalog:
            raise MethodNotFoundError(f"Method '{method}' not found in catalog.")

        return catalog[method]
