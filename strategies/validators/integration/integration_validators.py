import os

from app.utils.catalog_loader import load_catalog
from app.utils.rule_loader import load_rule
from core.exceptions import ValidationError


class IntegrationValidator:

    def __init__(self):
        base = os.path.dirname(__file__)
        path = os.path.join(base, "integration_validation_catalog.json")
        self.catalog = load_catalog(path)

    def validate(self, input_data):
        mode = input_data.get("mode")
        calculation_mode = input_data.get("calculation_mode")

        if mode != "function":
            raise ValidationError("Integration only supports mode='function'.")

        if calculation_mode not in self.catalog.get("supported_modes", []):
            raise ValidationError("Unsupported calculation_mode.")

        rules = self.catalog.get(calculation_mode).get("rules")
        if isinstance(rules, str):  # rule can be a single string or a list of strings
            rules = [rules]  # Convert to list for uniform processing
        for r in rules:
            # Load the custom validation rule
            validation_rule = load_rule(r)
            validation_rule(input_data)

        return True
