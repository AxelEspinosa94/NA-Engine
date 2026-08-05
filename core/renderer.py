
from __future__ import annotations
from typing import Any, Callable, Dict, List, Tuple, Union
import numpy as np

from core.RENDERER_META import RENDERER_META

def vector_to_latex(vec):
        body = " \\\\ ".join(str(x) for x in vec)
        return f"\\begin{{pmatrix}} {body} \\end{{pmatrix}}"

def matrix_to_latex(matrix):
    # Convertir a arreglo 2D normal
    arr = np.asarray(matrix)

    rows = []
    for row in arr:
        rows.append(" & ".join(f"{x:.6f}" for x in row))

    body = " \\\\ ".join(rows)
    return f"\\begin{{pmatrix}} {body} \\end{{pmatrix}}"


class Renderer:
    """
    Renderer for NA‑Engine.

    This class transforms raw executor outputs into standardized,
    UI‑friendly structures. It uses a two‑level dispatcher:

    1. Error detection (priority)
    2. Key‑based auto‑detection dispatcher
    3. Renderer‑type dispatcher (scalar, vector, matrix, plot, etc.)

    The goal is to keep the render() method declarative, scalable,
    and easy to extend when new modules or result types are added.
    """

    # ============================================================
    # Public API
    # ============================================================

    def render(self, calculation_mode: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Multi‑match renderer: detects ALL renderizable keys and returns
        a multi‑block payload instead of stopping at the first match.
        """

        # 1. Error has priority
        if "error" in result:
            return self.render_error(result)

        # 2. Renderer type dispatch
        type_dispatch = {
            "scalar": self.render_scalar,
            "vector": self.render_vector,
            "matrix": self.render_matrix_expression,
            "matrix_group": self.render_matrix_group,
            "table": self.render_table,
            "plot": self.render_plot,
            "markdown": self.render_markdown,
        }

        # 3. Key‑based detection rules
        KEY_DISPATCH = [
            ("derivative", "scalar"),
            ("second_derivative", "scalar"),
            ("third_derivative", "scalar"),
            ("value", "scalar"),
            ("inverse", "matrix"),
            ("determinant", "scalar"),
            ("norm", "scalar"),
            ("condition_number", "scalar"),
            ("transpose", "matrix"),
            ("rank", "scalar"),
            (("L", "U", "P"), "matrix_group"),
            ("L", "matrix"),
            ("matrix", "matrix"),
            (("Q", "R"), "matrix_group"),
            (("x", "y"), "plot"),
            (("x_nodes", "y_nodes"), "table"),
#            ("table", "table"),
            ("markdown", "markdown"),
            ("expression", "markdown"),
            ("solution", "vector"),
        ]

        # 4. Multi‑match accumulator
        blocks = []

        # 5. Iterate over detection rules
        for keys, renderer_type in KEY_DISPATCH:

            # Case: multiple keys must be present
            if isinstance(keys, tuple):
                if all(k in result for k in keys):

                    # plot(x,y)
                    if renderer_type == "plot":
                        blocks.append(
                            type_dispatch["plot"](result["x"], result["y"], label="curve")
                        )
                        continue

                    #table(x_nodes, y_nodes)
                    if renderer_type == "table":
                        blocks.append(
                            type_dispatch["table"]({
                                "columns": ["x", "y"],
                                "rows": list(zip(result["x_nodes"], result["y_nodes"]))
                            })
                        )
                        continue

                    # matrix_group(L,U,P)
                    blocks.append(type_dispatch[renderer_type](result))
                    continue

            # Case: single key
            else:
                if keys in result:
                    value = result[keys]

                    # matrix_group expects full dict
                    if renderer_type == "matrix_group":
                        blocks.append(type_dispatch[renderer_type](result))
                        continue

                    # plot(x,y)
                    if renderer_type == "plot":
                        blocks.append(
                            type_dispatch["plot"](result["x"], result["y"], label="curve")
                        )
                        continue

                    # table
                    if renderer_type == "table":
                        blocks.append(type_dispatch["table"](value))
                        continue

                    # markdown
                    if renderer_type == "markdown":
                        blocks.append(type_dispatch["markdown"](value))
                        continue

                    # scalar, vector, matrix
                    blocks.append(type_dispatch[renderer_type](value, label=keys))
                    continue

        # 6. If we detected blocks → return multi‑block payload
        if blocks:
            return {
                "type": "multi",
                "blocks": blocks
            }

        # 7. Fallback
        return {
            "type": "raw",
            "data": result
        }


    # ============================================================
    # Scalar Renderer
    # ============================================================

    def render_scalar(self, value: Any, label: str = "value") -> Dict[str, Any]:
        meta = RENDERER_META["scalar"]
        return {
            "type": "scalar",
            "label": label,
            "value": float(value),
            "caption": meta["caption"],
            "tooltip": meta["tooltip"]
        }


    # ============================================================
    # Vector Renderer
    # ============================================================

    def render_vector(self, vector: Union[List[Any], np.ndarray], label: str = "vector") -> Dict[str, Any]:
        """Render a 1D list or NumPy array."""
        meta = RENDERER_META["vector"]
        latex = vector_to_latex(vector)
        return {
            "type": "vector",
            "label": label,
            "latex": latex,
            "values": list(map(float, vector)),
            "caption": meta["caption"],
            "tooltip": meta["tooltip"]
        }

    # ============================================================
    # Matrix Renderer
    # ============================================================
    def render_matrix_expression(self, matrix, label="matrix"):
        latex = matrix_to_latex(matrix) 
        meta = RENDERER_META["matrix"]
        return {
            "type": "matrix_expression",
            "label": label,
            "latex": latex,
            "values": np.array(matrix).tolist(),
            "caption": meta["caption"],
            "tooltip": meta["tooltip"]
        }

    # ============================================================
    # Matrix Group Renderer (L, U, P)
    # ============================================================

    def render_matrix_group(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Render a group of matrices (e.g., L, U, P from LU decomposition),
        including both raw values and LaTeX expressions.
        """
        meta = RENDERER_META["matrix_group"]

        payload: Dict[str, Any] = {
            "type": "matrix_group",
            "caption": meta["caption"],
            "tooltip": meta["tooltip"],
            "matrices": {}
        }

        for key in ["L", "U", "P"]:
            if key in result:
                # Convert to array
                arr = np.asarray(result[key])
                # Raw values
                payload["matrices"][f"{key}_raw"] = arr.tolist()
                # LaTeX version
                payload["matrices"][f"{key}_latex"] = matrix_to_latex(arr)

        # Optional solution vector
        if "solution" in result:
            sol = np.asarray(result["solution"]).tolist()
            payload["solution"] = sol
            payload["solution_latex"] = vector_to_latex(sol)

        return payload


    # ============================================================
    # Table Renderer
    # ============================================================

    def render_table(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Render a table with columns and rows.

        Expected format:
        {
            "columns": [...],
            "rows": [[...], [...], ...]
        }
        """
        columns = result.get("columns", [])
        rows = result.get("rows", [])
        meta = RENDERER_META["table"]
        return {
            "type": "table",
            "columns": columns,
            "rows": rows,
            "caption": meta["caption"],
            "tooltip": meta["tooltip"]
        }

    # ============================================================
    # Plot Renderer
    # ============================================================

    def render_plot(self, x: List[Any], y: List[Any], label: str = "plot") -> Dict[str, Any]:
        """Render a curve defined by x and y arrays."""
        meta = RENDERER_META["plot"]
        return {
            "type": "plot",
            "label": label,
            "x": list(map(float, x)),
            "y": list(map(float, y)),
            "caption": meta["caption"],
            "tooltip": meta["tooltip"]
        }

    # ============================================================
    # Markdown Renderer
    # ============================================================

    def render_markdown(self, content: str) -> Dict[str, Any]:
        """Render markdown content."""
        meta = RENDERER_META["markdown"]
        
        return {
            "type": "markdown",
            "content": content,
            "caption": meta["caption"],
            "tooltip": meta["tooltip"]
        }

    # ============================================================
    # Error Renderer
    # ============================================================

    def render_error(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Render backend errors in a standardized format."""
        meta = RENDERER_META["error"]
        return {
            "type": "error",
            "message": result.get("error", "Unknown error"),
            "details": result.get("details", None),
            "caption": meta["caption"],
            "tooltip": meta["tooltip"]
        }
