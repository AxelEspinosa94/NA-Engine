from dash import ALL, Input, Output, Patch, State, ctx, html, no_update

from core.base_method import NumericalMethod
from core.contract import UIContract
from core.ui.styled_components import styled_input


def _build_mode_area(method: str, mode: str):
    return True


# Change it depending on how much stress the tool can handle. For example, if the tool can handle up to 10 dimensions, set MAX_DIM = 10. If it can handle up to 20 dimensions, set MAX_DIM = 20, etc.
MIN_DIM, MAX_DIM = 0, 10


def bound_row(i: int):
    return html.Div(
        className="input-row",
        children=[
            html.Div(f"x{i-1}", className="na-label bound-level"),
            styled_input(
                id={"type": "integr-a", "index": i}, type="number", placeholder="a"
            ),
            styled_input(
                id={"type": "integr-b", "index": i}, type="number", placeholder="b"
            ),
        ],
    )


contract = UIContract()


def register_integration_callbacks(app):

    # ============================================================
    # Callback 1: Construye el formulario dinámico
    # ============================================================
    @app.callback(
        Output("integr-mode-function", "hidden"),
        Output("integr-mode-gauss", "hidden"),
        Output("integr-btn-card", "hidden"),
        Input("integr-method", "value"),
        Input("integr-input-mode", "value"),
        prevent_initial_call=True,
    )
    def build_input_area(method, mode):

        if not method:
            return True, True, True

        # Área dinámica (siempre función)
        area = not _build_mode_area(method, mode)

        # Gauss-Legendre requiere puntos
        gauss_hidden = method != "gauss"

        # Botón visible
        btn_hidden = False

        return area, gauss_hidden, btn_hidden

    # ============================================================
    # Callback 2: Cambia la dimensión de la entrada
    # ============================================================

    @app.callback(
        Output("integr-bounds-rows", "children"),
        Output("integr-dim", "data"),
        Output("integr-add-dim", "disabled"),
        Output("integr-remove-dim", "disabled"),
        Input("integr-add-dim", "n_clicks"),
        Input("integr-remove-dim", "n_clicks"),
        State("integr-dim", "data"),
        prevent_initial_call=True,
    )
    def change_dimension(_add, _remove, dim):
        patch = Patch()

        if ctx.triggered_id == "integr-add-dim" and dim < MAX_DIM:
            patch.append(bound_row(dim))  # nueva fila con índice = dim actual
            dim += 1
        elif ctx.triggered_id == "integr-remove-dim" and dim > MIN_DIM:
            del patch[-1]
            dim -= 1
        else:
            return no_update, no_update, no_update, no_update

        return patch, dim, dim >= MAX_DIM, dim <= MIN_DIM

    # ============================================================
    # Callback 3: Ejecuta el cálculo
    # ============================================================
    @app.callback(
        Output("integr-result-area", "children"),
        Input("integr-run-btn", "n_clicks"),
        State("integr-method", "value"),
        State("integr-input-mode", "value"),
        State("integr-fn", "value"),
        State({"type": "integr-a", "index": ALL}, "value"),
        State({"type": "integr-b", "index": ALL}, "value"),
        State("integr-n", "value"),
        State("integr-gauss-points", "value"),
        prevent_initial_call=True,
    )
    def run_integration(n_clicks, method, mode, fn_expr, As, Bs, n, gauss_points=None):

        if not method or not fn_expr or As is None or Bs is None or n is None:
            return no_update

        bounds = [[a, b] for a, b in zip(As, Bs)]

        # Construir input_data para NumericalMethod
        input_data = {
            "mode": "function",
            "function": fn_expr,
            "bounds": bounds,
            "n": int(n),
            "calculation_mode": method,
        }

        if method == "gauss":
            input_data["gauss_points"] = int(gauss_points or 2)

        # Validación
        try:
            nm = NumericalMethod("integration", input_data)
            nm.validate_input()
        except Exception as e:
            return contract.resolve(
                method,
                {
                    "status": "error",
                    "error_type": "ValidationError",
                    "message": str(e),
                    "context": input_data,
                },
            )

        # Ejecución
        outcome = nm.execute()
        return contract.resolve(method, outcome)
