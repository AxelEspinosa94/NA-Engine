import pytest

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


# ============================================================
# Scalar Renderers
# ============================================================


def test_render_scalar_derivative(renderer):
    result = {"derivative": 0.5}
    rendered = renderer.render("central", result)

    block = rendered["blocks"][0]
    assert block["type"] == "scalar"
    assert block["label"] == "derivative"
    assert block["value"] == 0.5


def test_render_scalar_second_derivative(renderer):
    result = {"second_derivative": -3.14}
    rendered = renderer.render("second_central", result)

    block = rendered["blocks"][0]
    assert block["type"] == "scalar"
    assert block["label"] == "second_derivative"
    assert block["value"] == -3.14


# ============================================================
# Vector Renderer
# ============================================================


def test_render_vector(renderer):
    result = {"solution": [1, 2, 3]}
    rendered = renderer.render("gauss", result)

    block = rendered["blocks"][0]
    assert block["type"] == "vector"
    assert block["label"] == "solution"
    assert block["values"] == [1.0, 2.0, 3.0]


# ============================================================
# Matrix Renderer
# ============================================================


def test_render_matrix(renderer):
    result = {"inverse": [[1, 0], [0, 1]]}
    rendered = renderer.render("inverse", result)

    block = rendered["blocks"][0]
    assert block["type"] == "matrix_expression"
    assert block["label"] == "inverse"
    assert block["values"] == [[1, 0], [0, 1]]


# ============================================================
# Matrix Group Renderer (L, U, P)
# ============================================================


def test_render_matrix_group(renderer):
    result = {
        "L": [[1, 0], [2, 1]],
        "U": [[3, 4], [0, 5]],
        "P": [[0, 1], [1, 0]],
        "solution": [1, 2],
    }

    rendered = renderer.render("lu", result)
    blocks = rendered["blocks"]

    assert len(blocks[0].get("matrices")) == 6


# ============================================================
# Table Renderer
# ============================================================


def test_render_table(renderer):
    result = {
        "x_nodes": [0, 1],
        "y_nodes": [1, 2],
    }

    rendered = renderer.render("integration", result)
    blocks = rendered["blocks"][0]

    assert blocks["type"] == "table"
    assert blocks["columns"] == ["x", "y"]
    assert blocks["rows"] == [(0, 1), (1, 2)]


# ============================================================
# Plot Renderer
# ============================================================


def test_render_plot(renderer):
    result = {"x": [0, 1, 2], "y": [1, 2, 3]}

    rendered = renderer.render("rk4", result)
    block = rendered["blocks"][0]

    assert block["type"] == "plot"
    assert block["label"] == "curve"
    assert block["x"] == [0.0, 1.0, 2.0]
    assert block["y"] == [1.0, 2.0, 3.0]


# ============================================================
# Markdown Renderer
# ============================================================


def test_render_markdown(renderer):
    result = {"markdown": "### Title"}
    rendered = renderer.render("any", result)

    block = rendered["blocks"][0]
    assert block["type"] == "markdown"
    assert block["content"] == "### Title"


# ============================================================
# Fallback Renderer
# ============================================================


def test_render_raw(renderer):
    result = {"unexpected": 123}
    rendered = renderer.render("unknown", result)
    assert rendered["type"] == "raw"
    assert rendered["data"] == {"unexpected": 123}
