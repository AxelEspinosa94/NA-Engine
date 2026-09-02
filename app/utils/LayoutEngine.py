import os

from dash import html

from app.utils.catalog_loader import load_catalog
from app.utils.layout_catalog_loader import load_component
from core.exceptions import (
    CatalogLoadError,
    ConstructionError,
    ExecutionError,
    InputError,
    MethodNotFoundError,
    ValidationError,
)


class LayoutEngine:

    def __init__(self, base: str = None, module: str = None):
        self.module = module
        path = os.path.join(base, f"{self.module}_layout_catalog.json")
        self.catalog = load_catalog(path)
        self.custom_module = self.catalog.get("custom_module")
        self.method_selector_options = self.catalog.get("method_selector_options")

    def build(self):
        children = []

        # Header fijo
        children.append(
            html.Div(
                className="module-header",
                children=[
                    html.H2(self.catalog.get("header_contents").get("h2")),
                    html.P(self.catalog.get("header_contents").get("p")),
                ],
            )
        )

        # Declarative construction
        if "layout_structure" not in self.catalog:
            raise CatalogLoadError(
                f"Missing 'layout_structure' in catalog for module {self.module}"
            )

        for section in self.catalog["layout_structure"]:
            if section == "result_area":
                children.append(
                    html.Div(
                        id=f"{self.custom_module}-result-area", className="result-area"
                    )
                )
                continue

            # Cargar componente(s)
            comp_paths = self.catalog["component_map"].get(section, [])
            if isinstance(comp_paths, str):
                comp_paths = [comp_paths]

            for path in comp_paths:
                try:
                    component = load_component(path)
                except Exception as e:
                    raise CatalogLoadError(
                        f"Error loading component from path {path}: {e}"
                    )

                # Dynamic params
                params = self.catalog.get("component_params", {}).get(section, {})
                kwargs = {k: self.catalog[v] for k, v in params.items()}

                children.append(component(**kwargs))

        return html.Div(id=f"{self.custom_module}-container", children=children)
