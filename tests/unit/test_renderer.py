import pytest
import numpy as np
from core.renderer import Renderer


@pytest.fixture
def renderer():
    return Renderer()


# ============================================================
# Error Renderer
# ============================================================

def test_render_error(renderer):
    result = {"error": "Something went wrong", "details": "Division by zero"}
    rendered = renderer.render("any_mode", result)

    assert rendered["type"] == "error"
    assert rendered["message"] == "Something went wrong"
    assert rendered["details"] == "Division by zero"


# ============================================================
# Scalar Renderers
# ============================================================

def test_render_scalar_derivative(renderer):
    result = {"derivative": 0.5}
    rendered = renderer.render("central", result)

    assert rendered["type"] == "scalar"
    assert rendered["label"] == "derivative"
    assert rendered["value"] == 0.5


def test_render_scalar_second_derivative(renderer):
    result = {"second_derivative": -3.14}
    rendered = renderer.render("second_central", result)

    assert rendered["type"] == "scalar"
    assert rendered["label"] == "second_derivative"
    assert rendered["value"] == -3.14


# ============================================================
# Vector Renderer
# ============================================================

def test_render_vector(renderer):
    result = {"solution": [1, 2, 3]}
    rendered = renderer.render("gauss", result)

    assert rendered["type"] == "vector"
    assert rendered["label"] == "solution"
    assert rendered["values"] == [1.0, 2.0, 3.0]


# ============================================================
# Matrix Renderer
# ============================================================

def test_render_matrix(renderer):
    result = {"inverse": [[1, 0], [0, 1]]}
    rendered = renderer.render("inverse", result)

    assert rendered["type"] == "matrix"
    assert rendered["label"] == "inverse"
    assert rendered["values"] == [[1, 0], [0, 1]]


# ============================================================
# Matrix Group Renderer (L, U, P)
# ============================================================

def test_render_matrix_group(renderer):
    result = {
        "L": [[1, 0], [2, 1]],
        "U": [[3, 4], [0, 5]],
        "P": [[0, 1], [1, 0]],
        "solution": [1, 2]
    }

    rendered = renderer.render("lu", result)

    assert rendered["type"] == "matrix_group"
    assert rendered["L"] == [[1, 0], [2, 1]]
    assert rendered["U"] == [[3, 4], [0, 5]]
    assert rendered["P"] == [[0, 1], [1, 0]]
    assert rendered["solution"] == [1.0, 2.0]


# ============================================================
# Table Renderer
# ============================================================

def test_render_table(renderer):
    result = {
        "table": {
            "columns": ["x", "y"],
            "rows": [[0, 1], [1, 2]]
        }
    }

    rendered = renderer.render("integration", result)

    assert rendered["type"] == "table"
    assert rendered["columns"] == ["x", "y"]
    assert rendered["rows"] == [[0, 1], [1, 2]]


# ============================================================
# Plot Renderer
# ============================================================

def test_render_plot(renderer):
    result = {
        "x": [0, 1, 2],
        "y": [1, 2, 3]
    }

    rendered = renderer.render("rk4", result)

    assert rendered["type"] == "plot"
    assert rendered["label"] == "curve"
    assert rendered["x"] == [0.0, 1.0, 2.0]
    assert rendered["y"] == [1.0, 2.0, 3.0]


# ============================================================
# Markdown Renderer
# ============================================================

def test_render_markdown(renderer):
    result = {"markdown": "### Title"}
    rendered = renderer.render("any", result)

    assert rendered["type"] == "markdown"
    assert rendered["content"] == "### Title"


# ============================================================
# Fallback Renderer
# ============================================================

def test_render_raw(renderer):
    result = {"unexpected": 123}
    rendered = renderer.render("unknown", result)

    assert rendered["type"] == "raw"
    assert rendered["data"] == {"unexpected": 123}
