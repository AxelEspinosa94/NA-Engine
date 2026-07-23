# callbacks/ode_callbacks.py

from dash import Input, Output, State, html, dcc
from core.base_method import NumericalMethod
from core.contract import UIContract

contract = UIContract()


# ═══════════════════════════════════════════════════════════════
# 1. Callback — Construcción dinámica del área de inputs
# ═══════════════════════════════════════════════════════════════
def register_ode_callbacks(app):

    @app.callback(
        [
            Output("ode-function-card", "hidden"),
            Output("ode-system-card", "hidden"),
            Output("ode-ivp-card", "hidden"),
            Output("ode-system-y0-card", "hidden"),
            Output("ode-shooting-card", "hidden"),
            Output("ode-fd-card", "hidden"),
            Output("ode-btn-card", "hidden"),
        ],
        [
            Input("ode-method", "value"),
            Input("ode-input-mode", "value"),
        ],
    )
    def _build_input_area(method, input_mode):

        # No method selected yet
        if method is None:
            return True, True, True, True, True, True, True

        # ───────────────────────────────────────────────
        # Mostrar/ocultar tarjetas según calculation_mode
        # ───────────────────────────────────────────────

        # IVP methods
        ivp_modes = {
            "euler", "heun", "rk2", "rk4",
            "adams_bashforth_2", "adams_bashforth_3", "adams_moulton_2"
        }

        # System ODE
        system_modes = {"rk4_system"}

        # Shooting BVP
        shooting_modes = {"shooting"}

        # Finite differences BVP
        fd_modes = {"finite_differences"}

        if input_mode == "function":
            show_function = True
        elif input_mode == "system":
            show_function = False

        show_ivp = method in ivp_modes
        show_system = method in system_modes
        show_shooting = method in shooting_modes
        show_fd = method in fd_modes

        # Botón visible si hay método válido
        show_btn = True

        return (
            not show_function,
            not show_system,
            not show_ivp,
            not show_system,
            not show_shooting,
            not show_fd,
            not show_btn,
        )

    # ═══════════════════════════════════════════════════════════════
    # 2. Callback — Ejecutar ODE
    # ═══════════════════════════════════════════════════════════════
    @app.callback(
        Output("ode-result-area", "children"),
        Input("ode-run-btn", "n_clicks"),
        [
            State("ode-method", "value"),
            State("ode-input-mode", "value"),
            State("ode-function", "value"),
            State("ode-system", "value"),
            State("ode-x0", "value"),
            State("ode-y0", "value"),
            State("ode-x-end", "value"),
            State("ode-h", "value"),
            State("ode-y0-system", "value"),
            State("ode-alpha", "value"),
            State("ode-beta", "value"),
            State("ode-s0", "value"),
            State("ode-alpha-fd", "value"),
            State("ode-beta-fd", "value"),
            State("ode-n", "value"),
        ],
    )
    def run_ode(
        n_clicks,
        method,
        input_mode,
        function,
        system,
        x0,
        y0,
        x_end,
        h,
        y0_system,
        alpha,
        beta,
        s0,
        alpha_fd,
        beta_fd,
        n_fd,
    ):

        if not n_clicks:
            return ""

        # ───────────────────────────────────────────────
        # Construcción del input_data
        # ───────────────────────────────────────────────
        input_data = {
            "calculation_mode": method,
        }

        # Modo función
        if input_mode == "function":
            input_data["function"] = function

        # Modo sistema
        else:
            if system:
                system_list = [line.strip() for line in system.split("\n") if line.strip()]
                input_data["system"] = system_list

            if y0_system:
                y0_list = [float(v.strip()) for v in y0_system.split(",")]
                input_data["y0"] = y0_list

        # IVP fields
        if method in {
            "euler", "heun", "rk2", "rk4",
            "adams_bashforth_2", "adams_bashforth_3", "adams_moulton_2"
        }:
            input_data["x0"] = x0
            input_data["y0"] = y0
            input_data["x_end"] = x_end
            input_data["h"] = h

        # System ODE
        if method == "rk4_system":
            input_data["x0"] = x0
            input_data["x_end"] = x_end
            input_data["h"] = h

        # Shooting BVP
        if method == "shooting":
            input_data["x0"] = x0
            input_data["x_end"] = x_end
            input_data["alpha"] = alpha
            input_data["beta"] = beta
            input_data["s0"] = s0
            input_data["h"] = h

        # Finite differences BVP
        if method == "finite_differences":
            input_data["x0"] = x0
            input_data["x_end"] = x_end
            input_data["alpha"] = alpha_fd
            input_data["beta"] = beta_fd
            input_data["n"] = n_fd
            input_data["function"] = function

        # ───────────────────────────────────────────────
        # Ejecutar NumericalMethod
        # ───────────────────────────────────────────────
        try:
            nm = NumericalMethod("ode", input_data)
            nm.validate_input()
            outcome = nm.execute()
        except Exception as e:
            return html.Div(
                className="error",
                children=f"Error: {str(e)}"
            )

        # ───────────────────────────────────────────────
        # Resolver UIContract
        # ───────────────────────────────────────────────
        payload = contract.resolve(method, outcome)
        return payload
