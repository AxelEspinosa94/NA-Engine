# tests/integration/test_interpolation.py
import pytest
import pandas as pd
from core.base_method import NumericalMethod
from core.contract import UIContract
from dash import html

contract = UIContract()


@pytest.fixture
def lagrange_outcome():
    """Ejecuta el método real y devuelve el outcome."""
    input_data = {
        "mode": "table",
        "data": pd.DataFrame({"x": [0, 1, 2], "y": [0, 1, 4]}),
        "xk": 1.5,
        "calculation_mode": "lagrange"
    }
    nm = NumericalMethod("interpolation", input_data)
    nm.validate_input()
    return nm.execute(), "lagrange"


def test_lagrange_devuelve_div(lagrange_outcome):
    outcome, mode = lagrange_outcome
    result = contract.resolve(mode, outcome)
    assert isinstance(result, html.Div)


def test_lagrange_status_success(lagrange_outcome):
    outcome, _ = lagrange_outcome
    assert outcome["status"] == "success"


def test_lagrange_result_tiene_valor(lagrange_outcome):
    outcome, _ = lagrange_outcome
    # el executor de lagrange debería devolver algo reconocible
    assert "value" in outcome["result"]

# tests/integration/test_interpolation.py  (continuación)
from core.exceptions import ValidationError
# helper para aplanar el árbol de componentes Dash
def _flatten_children(component):
    items = []
    if hasattr(component, "children") and component.children:
        children = component.children
        if not isinstance(children, list):
            children = [children]
        for child in children:
            items.append(child)
            items.extend(_flatten_children(child))
    return items

def test_lagrange_input_invalido_devuelve_error_div():
    input_data = {"calculation_mode": "lagrange", "mode": "table", "data": pd.DataFrame(), "xk": 1.5}  # df vacío
    nm = NumericalMethod("interpolation", input_data)

    try:
        nm.validate_input()
        outcome = nm.execute()
    except ValidationError as e:
        outcome = {
            "status":     "error",
            "error_type": "ValidationError",
            "message":    str(e),
            "context":    input_data,
        }

    result = contract.resolve(input_data["mode"], outcome)
    assert isinstance(result, html.Div)
    flat = _flatten_children(result)
    assert any("error" in str(c).lower() for c in flat)