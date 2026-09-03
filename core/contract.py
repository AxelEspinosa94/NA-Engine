# core/contract.py
from typing import Any, Dict

from dash import dcc, html

from app.components.result_view import build_result_view
from core.renderer import Renderer
from core.ui.tooltips import Tooltip


class UIContract:
    def __init__(self, renderer: Renderer | None = None) -> None:
        self.renderer = renderer or Renderer()

    def resolve(self, calculation_mode: str, outcome: Dict[str, Any]) -> html.Div:
        if outcome.get("status") == "error":
            payload = self.renderer.render(
                calculation_mode,
                {
                    "error": outcome.get("message", "Unknown error"),
                    "details": {
                        "error_type": outcome.get("error_type"),
                        "context": outcome.get("context"),
                    },
                },
            )
            return build_result_view(payload)

        payload = self.renderer.render(calculation_mode, outcome.get("result", {}))

        # resultado compuesto: construir bloques independientes
        blocks = self._build_blocks(calculation_mode, payload)

        return html.Div(blocks, className="result-container")

    # ------------------------------------------------------------------
    # Bloques
    # ------------------------------------------------------------------
    def _build_blocks(self, calculation_mode: str, result: Dict[str, Any]) -> list:
        blocks = []

        for block in result.get("blocks", []):
            block_type = block.get("type")
            if block_type == "scalar":
                blocks.append(self._block_value(calculation_mode, block))
            elif block_type == "markdown":
                blocks.append(self._block_expression(block))
            elif block_type == "table":
                blocks.append(self._block_table(block))
            elif block_type == "plot":
                blocks.append(self._block_plot(block))
            elif block_type == "vector":
                blocks.append(self._block_solution(block))
            elif block_type == "matrix_expression":
                blocks.append(self._block_matrix_expression(block))
            elif block_type == "matrix_group":
                blocks.append(self._block_matrix_group(block))
            else:
                # Bloque desconocido, renderizar como raw
                blocks.append(build_result_view(block))

        return blocks

    def _block_plot(self, payload: Dict[str, Any]) -> html.Div:
        import plotly.graph_objects as go
        from dash import dcc

        fig = go.Figure()
        caption = payload.get("caption", "Gráfica")
        tooltip = payload.get("tooltip", "")
        # Curva del polinomio
        fig.add_trace(
            go.Scatter(
                x=payload["x"],
                y=payload["y"],
                mode="lines",
                name="P(x)",
                line=dict(color="#dec6e5", width=2),
            )
        )

        # Nodos originales del df
        if "x_nodes" in payload and "y_nodes" in payload:
            fig.add_trace(
                go.Scatter(
                    x=payload["x_nodes"],
                    y=payload["y_nodes"],
                    mode="markers",
                    name="Nodos",
                    marker=dict(color="#e5c07b", size=8, symbol="circle"),
                )
            )

        fig.update_layout(
            template="plotly_dark",
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis_title="x",
            yaxis_title="P(x)",
            legend=dict(orientation="h", y=-0.2),
        )

        return html.Div(
            [
                html.Div(
                    className="label-with-tooltip",
                    children=[
                        dcc.Markdown(caption, className="result-explanation"),
                        Tooltip(tooltip).render() if tooltip else None,
                    ],
                ),
                dcc.Graph(figure=fig, className="result-plot"),
            ]
        )

    # ------------------------------------------------------------------
    # Builders de bloques individuales
    # ------------------------------------------------------------------

    def _block_value(self, method: str, payload: Dict[str, Any]) -> html.Div:
        caption = payload.get("caption", "Resultado")
        tooltip = payload.get("tooltip", "")
        value = payload.get("value", None)
        md = f"$$f(x_k) = \\boxed{{{float(value):.6g}}}$$\n\n" f"Método: **{method}**"
        return html.Div(
            [
                html.Div(
                    className="label-with-tooltip",
                    children=[
                        dcc.Markdown(caption, className="result-explanation"),
                        Tooltip(tooltip).render() if tooltip else None,
                    ],
                ),
                dcc.Markdown(md, className="result-explanation", mathjax=True),
            ]
        )

    def _block_expression(self, payload: Dict[str, Any]) -> html.Div:
        caption = payload.get("caption", "Resultado")
        tooltip = payload.get("tooltip", "")
        expression = payload["content"]

        md = f"```\n{expression}\n```"

        return html.Div(
            [
                html.Div(
                    className="label-with-tooltip",
                    children=[
                        dcc.Markdown(caption, className="result-explanation"),
                        Tooltip(tooltip).render() if tooltip else None,
                    ],
                ),
                dcc.Markdown(md, className="result-expression"),
            ]
        )

    def _block_table(self, payload: Dict[str, Any]) -> html.Div:
        caption = payload.get("caption", "Tabla de resultados")
        tooltip = payload.get("tooltip", "")
        columns = payload.get("columns", [])
        rows = payload.get("rows", [])

        p = {"type": "table", "columns": columns, "rows": rows}
        return html.Div(
            [
                html.Div(
                    className="label-with-tooltip",
                    children=[
                        dcc.Markdown(caption, className="result-explanation"),
                        Tooltip(tooltip).render() if tooltip else None,
                    ],
                ),
                build_result_view(p),
            ]
        )

    def _block_matrix_expression(self, payload: Dict[str, Any]) -> html.Div:
        caption = payload.get("caption", "Matriz")
        tooltip = payload.get("tooltip", "")
        expression = payload["latex"]

        md = f"$$\n{expression}\n$$"

        return html.Div(
            [
                html.Div(
                    className="label-with-tooltip",
                    children=[
                        dcc.Markdown(caption, className="result-explanation"),
                        Tooltip(tooltip).render() if tooltip else None,
                    ],
                ),
                dcc.Markdown(md, className="result-expression", mathjax=True),
            ]
        )

    def _block_matrix_group(self, payload: Dict[str, Any]) -> html.Div:
        caption = payload.get("caption", "Matrices")
        tooltip = payload.get("tooltip", "")
        matrices = payload.get("matrices", [])

        blocks = []
        for key, matrix in matrices.items():
            if key.endswith("_latex"):
                matrix_name = key.replace("_latex", "")
                expression = matrix
                md = f"$$\n{matrix_name} = {expression}\n$$"
                blocks.append(
                    dcc.Markdown(md, className="result-expression", mathjax=True)
                )

        return html.Div(
            [
                html.Div(
                    className="label-with-tooltip",
                    children=[
                        dcc.Markdown(caption, className="result-explanation"),
                        Tooltip(tooltip).render() if tooltip else None,
                    ],
                ),
                html.Div(blocks, className="matrix-group"),
            ]
        )

    def _block_solution(self, payload: Dict[str, Any]) -> html.Div:
        caption = payload.get("caption", "Solución")
        tooltip = payload.get("tooltip", "")
        solution = payload.get("latex", [])

        md = f"$$\n\\text{{Solución: }} {solution}\n$$"

        return html.Div(
            [
                html.Div(
                    className="label-with-tooltip",
                    children=[
                        dcc.Markdown(caption, className="result-explanation"),
                        Tooltip(tooltip).render() if tooltip else None,
                    ],
                ),
                dcc.Markdown(md, className="result-expression", mathjax=True),
            ]
        )
