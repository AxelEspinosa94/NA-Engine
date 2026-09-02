import os

import numpy as np
import pandas as pd

from app.utils.catalog_loader import load_catalog
from app.utils.rule_loader import load_rule
from core.exceptions import ExecutionError

from .payload import build_payload


class IntegrationExecutor:

    def __init__(self):
        base = os.path.dirname(__file__)
        path = os.path.join(base, "integration_executors_catalog.json")
        self.catalog = load_catalog(path)

    def run(self, instance):

        calculation_mode = instance.calculation_mode

        if calculation_mode not in self.catalog.get("supported_modes", []):
            raise ExecutionError("Unsupported calculation_mode.")

        exec = self.catalog.get(calculation_mode).get("executor")
        execute = load_rule(exec)
        value = execute(instance)
        return build_payload(instance, value)
