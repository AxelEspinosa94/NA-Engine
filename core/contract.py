# core/contract.py
from typing import Dict, Any, Optional
from app.components.result_view import build_result_view
from core.renderer import Renderer
from dash import html, dcc

class UIContract:
    def __init__(self, renderer: Renderer | None = None) -> None:
        self.renderer = renderer or Renderer()

    def resolve(self, calculation_mode: str, outcome: Dict[str, Any]) -> html.Div:
        if outcome.get("status") == "error":
            payload = self.renderer.render(calculation_mode, {
                "error": outcome.get("message", "Unknown error"),
                "details": {
                    "error_type": outcome.get("error_type"),
                    "context":    outcome.get("context"),
                },
            })
            return build_result_view(payload)

        result = outcome.get("result", {})

        # resultado compuesto: construir bloques independientes
        blocks = self._build_blocks(calculation_mode, result)

        return html.Div(blocks, className="result-container")

    # ------------------------------------------------------------------
    # Bloques
    # ------------------------------------------------------------------

    def _build_blocks(self, calculation_mode: str, result: Dict[str, Any]) -> list:
        """
        Inspecciona result y construye una lista ordenada de componentes Dash.
        Cada clave conocida genera su propio bloque.
        """
        blocks = []

        # 1. Valor numérico principal
        if "value" in result:
            blocks.append(self._block_value(calculation_mode, result))

        # 2. Expresión simbólica / polinomio
        if "expression" in result:
            blocks.append(self._block_expression(result["expression"]))

        # 3. Tabla
        if "table" in result:
            blocks.append(self._block_table(result["table"]))

        # 4. Plot (si el executor devuelve x, y)
        if "x" in result and "y" in result:
            payload = self.renderer.render(calculation_mode, result)
            blocks.append(build_result_view(payload))

        # 5. Solución vectorial
        if "solution" in result and "value" not in result:
            payload = self.renderer.render(calculation_mode, result)
            blocks.append(build_result_view(payload))

        # fallback
        if not blocks:
            payload = self.renderer.render(calculation_mode, result)
            blocks.append(build_result_view(payload))

        return blocks

    # ------------------------------------------------------------------
    # Builders de bloques individuales
    # ------------------------------------------------------------------

    def _block_value(self, method: str, result: Dict[str, Any]) -> html.Div:
        value = result["value"]
        md = (
            f"### Resultado\n\n"
            f"$$f(x_k) = \\boxed{{{float(value):.6g}}}$$\n\n"
            f"Método: **{method}**"
        )
        return html.Div([
            dcc.Markdown(md, className="result-explanation", mathjax=True),
        ])

    def _block_expression(self, expression: str) -> html.Div:
        md = f"### Polinomio\n\n```\n{expression}\n```"
        return html.Div([
            dcc.Markdown(md, className="result-expression"),
        ])

    def _block_table(self, table: Any) -> html.Div:
        # table puede llegar como DataFrame o como dict {columns, rows}
        if hasattr(table, "to_dict"):  # es DataFrame
            columns = list(table.columns)
            rows    = table.values.tolist()
        else:
            columns = table.get("columns", [])
            rows    = table.get("rows", [])

        payload = {"type": "table", "columns": columns, "rows": rows}
        return html.Div([
            dcc.Markdown("### Tabla de nodos", className="result-explanation"),
            build_result_view(payload),
        ])