# app/callbacks/integration_callbacks.py
from dash import Input, Output, State, callback
from core.base_method import NumericalMethod
from core.contract import UIContract
from core.exceptions import ValidationError

contract = UIContract()

@callback(
    Output("integration-result-area", "children"),
    Input("integration-run-btn", "n_clicks"),
    State("integration-method", "value"),
    # ... states del formulario
    prevent_initial_call=True,
)
def run_integration(n_clicks, method, *args):
    input_data = {}  # armar desde args
    try:
        nm = NumericalMethod(method, input_data)
        nm.validate_input()
    except ValidationError as e:
        return contract.resolve(method, {
            "status":     "error",
            "error_type": "ValidationError",
            "message":    str(e),
            "context":    input_data,
        })

    outcome = nm.execute()
    return contract.resolve(method, outcome)