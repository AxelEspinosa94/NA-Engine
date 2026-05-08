from dash import Input, Output, callback


def register_theme_callbacks(app):

    @app.callback(
        Output("app-container", "className"),
        Input("toggle-theme", "n_clicks"),
        prevent_initial_call=True
    )
    def toggle_theme(n):
        if n and n % 2 == 1:
            return "dark"
        return ""
