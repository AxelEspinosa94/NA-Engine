# tests/unit/test_contract.py
import pytest
from unittest.mock import MagicMock
from core.contract import UIContract
from dash import html


@pytest.fixture
def contract():
    return UIContract()


def test_resolve_error(contract):
    outcome = {
        "status":     "error",
        "error_type": "ValidationError",
        "message":    "Datos inválidos",
        "context":    {"x": []},
    }
    result = contract.resolve("lagrange", outcome)
    assert isinstance(result, html.Div)
    # buscar el mensaje de error en el árbol de children
    flat = _flatten_children(result)
    assert any("Datos inválidos" in str(c) for c in flat)


def test_resolve_scalar(contract):
    outcome = {
        "status": "success",
        "message": "",
        "context": {},
        "result": {"derivative": 3.14},
    }
    result = contract.resolve("central", outcome)
    assert isinstance(result, html.Div)


def test_resolve_plot(contract):
    outcome = {
        "status": "success",
        "message": "",
        "context": {},
        "result": {"x": [0.0, 1.0, 2.0], "y": [0.0, 1.0, 4.0]},
    }
    result = contract.resolve("rk4", outcome)
    assert isinstance(result, html.Div)


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