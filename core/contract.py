# core/contract.py
from typing import Any, Dict
from core.renderer import Renderer
from app.components.result_view import build_result_view
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

        result  = outcome.get("result", {})
        message = outcome.get("message", "")
        payload = self.renderer.render(calculation_mode, result)

        explanation = self._build_explanation(
            method=calculation_mode,
            input_data=outcome.get("context", {}),
            result=result,
            payload=payload,
        )

        children = []
        if explanation:
            children.append(dcc.Markdown(
                explanation,
                className="result-explanation",
                mathjax=True,
            ))
        if message:
            children.append(dcc.Markdown(message, className="result-message"))

        children.append(html.Hr())
        children.append(build_result_view(payload))

        return html.Div(children, className="result-container")

    # ------------------------------------------------------------------
    # Explicaciones por tipo
    # ------------------------------------------------------------------

    def _build_explanation(self, method, input_data, result, payload) -> str:
        builders = {
            "scalar":       self._explain_scalar,
            "vector":       self._explain_vector,
            "matrix":       self._explain_matrix,
            "matrix_group": self._explain_matrix_group,
            "table":        self._explain_table,
            "plot":         self._explain_plot,
        }
        fn = builders.get(payload["type"], self._explain_generic)
        return fn(method, input_data, result, payload)

    def _explain_scalar(self, method, input_data, result, payload) -> str:
        return (
            f"### Resultado: `{payload['label']}`\n\n"
            f"Usando el método **{method}**, se obtuvo:\n\n"
            f"$$\\boxed{{{payload['value']:.6g}}}$$"
        )

    def _explain_vector(self, method, input_data, result, payload) -> str:
        values = ",\\ ".join(f"{v:.4g}" for v in payload["values"])
        return (
            f"### Solución vectorial\n\n"
            f"El método **{method}** retornó:\n\n"
            f"$$x = [{values}]$$"
        )

    def _explain_matrix(self, method, input_data, result, payload) -> str:
        return (
            f"### Matriz: `{payload['label']}`\n\n"
            f"Resultado del método **{method}**."
        )

    def _explain_matrix_group(self, method, input_data, result, payload) -> str:
        keys = [k for k in ["L", "U", "P"] if k in payload]
        return (
            f"### Descomposición **{method.upper()}**\n\n"
            f"Matrices obtenidas: {', '.join(f'**{k}**' for k in keys)}."
        )

    def _explain_table(self, method, input_data, result, payload) -> str:
        n = len(payload.get("rows", []))
        return (
            f"### Tabla de resultados\n\n"
            f"El método **{method}** generó **{n} filas**."
        )

    def _explain_plot(self, method, input_data, result, payload) -> str:
        x = payload["x"]
        return (
            f"### Curva generada\n\n"
            f"Intervalo $[{x[0]:.4g},\\ {x[-1]:.4g}]$ "
            f"con **{len(x)} puntos**."
        )

    def _explain_generic(self, method, input_data, result, payload) -> str:
        return f"### Resultado\n\nMétodo: **{method}**."