from dash import Dash
from .layout.base_layout import layout
from .callbacks.theme_callbacks import register_theme_callbacks
from .callbacks.navigation_callbacks import register_navigation_callbacks
from .callbacks.interpolation_callbacks import register_interpolation_callbacks
from .callbacks.integration_callbacks import register_integration_callbacks
from .callbacks.linear_algebra_callbacks import register_linear_algebra_callbacks
from .callbacks.numerical_derivative_callbacks import register_derivative_callbacks
from .callbacks.non_linear_callbacks import register_nonlinear_callbacks
from .callbacks.ode_callbacks import register_ode_callbacks
from .callbacks.docs_callbacks import register_docs_callbacks


def create_app():
    app = Dash(__name__, suppress_callback_exceptions=True, assets_folder="./assets")

    app.layout = layout

    register_theme_callbacks(app)
    register_navigation_callbacks(app)
    register_interpolation_callbacks(app)
    register_integration_callbacks(app)
    register_linear_algebra_callbacks(app)
    register_derivative_callbacks(app)
    register_nonlinear_callbacks(app)
    register_ode_callbacks(app)
    register_docs_callbacks(app)

    return app
