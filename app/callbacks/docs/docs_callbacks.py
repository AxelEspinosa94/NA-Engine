from dash import Input, Output, State, dcc

from app.callbacks.docs.components.methods import load_methods


def register_docs_callbacks(app):

    @app.callback(
        Output("docs-method", "options"),
        Input("docs-module", "value"),
    )
    def update_methods(module):
        if module is None:
            return []

        try:
            methods = load_methods(module)
        except Exception as e:
            raise e

        return methods

    @app.callback(
        Output("docs-btn-card", "hidden"),
        Input("docs-method", "value"),
    )
    def show_button(method):
        return method is None

    @app.callback(
        Output("docs-result-area", "children"),
        Input("docs-run-btn", "n_clicks"),
        State("docs-module", "value"),
        State("docs-method", "value"),
        prevent_initial_call=True,
    )
    def render_docs(n_clicks, module, method):

        md_path = f"docs/theory/{module}/theory_{method}.md"

        with open(md_path, "r", encoding="utf-8") as f:
            raw_md = f.read()

        # Inyectar HTML crudo (MathJax lo detecta)
        return dcc.Markdown(children=raw_md, className="markdown-doc", mathjax=True)
