
from __future__ import annotations
from typing import Any, Callable, Dict, List, Tuple, Union
import numpy as np


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
        Main dispatcher. Detects the type of result and routes it to the correct renderer.

        Parameters
        ----------
        calculation_mode : str
            The backend method used (e.g., "rk4", "gauss", "central").
            Currently unused, but kept for future extensibility.

        result : dict
            Raw output from the executor.

        Returns
        -------
        dict
            A standardized UI‑friendly payload.
        """

        # --------------------------------------------------------
        # 1. Error always has priority
        # --------------------------------------------------------
        if "error" in result:
            return self.render_error(result)

        # --------------------------------------------------------
        # 2. Renderer‑type dispatcher
        # --------------------------------------------------------
        type_dispatch: Dict[str, Callable[..., Dict[str, Any]]] = {
            "scalar": self.render_scalar,
            "vector": self.render_vector,
            "matrix": self.render_matrix,
            "matrix_group": self.render_matrix_group,
            "table": self.render_table,
            "plot": self.render_plot,
            "markdown": self.render_markdown,
        }

        # --------------------------------------------------------
        # 3. Key‑based auto‑detection dispatcher
        #
        # Each entry is:
        #   (keys, renderer_type)
        #
        # where:
        #   - keys: str → single key must exist
        #   - keys: tuple → ALL keys must exist
        # --------------------------------------------------------
        KEY_DISPATCH: List[Tuple[Union[str, Tuple[str, ...]], str]] = [
            ("derivative", "scalar"),
            ("second_derivative", "scalar"),
            ("third_derivative", "scalar"),
            ("inverse", "matrix"),
            (("L", "U", "P"), "matrix_group"),
            (("x", "y"), "plot"),
            ("table", "table"),
            ("markdown", "markdown"),
            ("solution", "vector"),
        ]

        # --------------------------------------------------------
        # 4. Iterate over detection rules
        # --------------------------------------------------------
        for keys, renderer_type in KEY_DISPATCH:

            # Case: multiple keys must be present (e.g., L/U/P or x/y)
            if isinstance(keys, tuple):
                if all(k in result for k in keys):
                    if renderer_type == "plot":
                        return type_dispatch["plot"](result["x"], result["y"], label="curve")
                    return type_dispatch[renderer_type](result)


            # Case: single key
            else:
                if keys in result:
                    value = result[keys]

                    # matrix_group expects the full result dict
                    if renderer_type == "matrix_group":
                        return type_dispatch[renderer_type](result)

                    # plot expects x and y separately
                    if renderer_type == "plot":
                        return type_dispatch["plot"](result["x"], result["y"], label="curve")

                    # table expects a dict with columns/rows
                    if renderer_type == "table":
                        return type_dispatch["table"](value)

                    # markdown expects a string
                    if renderer_type == "markdown":
                        return type_dispatch["markdown"](value)

                    # scalar, vector, matrix
                    return type_dispatch[renderer_type](value, label=keys)

        # --------------------------------------------------------
        # 5. Fallback: raw data (unknown structure)
        # --------------------------------------------------------
        return {
            "type": "raw",
            "data": result
        }

    # ============================================================
    # Scalar Renderer
    # ============================================================

    def render_scalar(self, value: Any, label: str = "value") -> Dict[str, Any]:
        """Render a single numeric value."""
        return {
            "type": "scalar",
            "label": label,
            "value": float(value)
        }

    # ============================================================
    # Vector Renderer
    # ============================================================

    def render_vector(self, vector: Union[List[Any], np.ndarray], label: str = "vector") -> Dict[str, Any]:
        """Render a 1D list or NumPy array."""
        return {
            "type": "vector",
            "label": label,
            "values": list(map(float, vector))
        }

    # ============================================================
    # Matrix Renderer
    # ============================================================

    def render_matrix(self, matrix: Any, label: str = "matrix") -> Dict[str, Any]:
        """Render a 2D matrix."""
        return {
            "type": "matrix",
            "label": label,
            "values": np.array(matrix).tolist()
        }

    # ============================================================
    # Matrix Group Renderer (L, U, P)
    # ============================================================

    def render_matrix_group(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Render a group of matrices (e.g., L, U, P from LU decomposition).
        """
        payload: Dict[str, Any] = {"type": "matrix_group"}

        for key in ["L", "U", "P"]:
            if key in result:
                payload[key] = np.array(result[key]).tolist()

        if "solution" in result:
            payload["solution"] = list(map(float, result["solution"]))

        return payload

    # ============================================================
    # Table Renderer
    # ============================================================

    def render_table(self, table: Dict[str, Any]) -> Dict[str, Any]:
        """
        Render a table with columns and rows.

        Expected format:
        {
            "columns": [...],
            "rows": [[...], [...], ...]
        }
        """
        return {
            "type": "table",
            "columns": table.get("columns", []),
            "rows": table.get("rows", [])
        }

    # ============================================================
    # Plot Renderer
    # ============================================================

    def render_plot(self, x: List[Any], y: List[Any], label: str = "plot") -> Dict[str, Any]:
        """Render a curve defined by x and y arrays."""
        return {
            "type": "plot",
            "label": label,
            "x": list(map(float, x)),
            "y": list(map(float, y))
        }

    # ============================================================
    # Markdown Renderer
    # ============================================================

    def render_markdown(self, content: str) -> Dict[str, Any]:
        """Render markdown content."""
        return {
            "type": "markdown",
            "content": content
        }

    # ============================================================
    # Error Renderer
    # ============================================================

    def render_error(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Render backend errors in a standardized format."""
        return {
            "type": "error",
            "message": result.get("error", "Unknown error"),
            "details": result.get("details", None)
        }
