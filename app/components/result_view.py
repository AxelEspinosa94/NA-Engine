# app/components/result_view.py
from dash import html, dcc
import plotly.graph_objects as go
from dash import dash_table


def build_result_view(payload: dict) -> html.Div:
    renderers = {
        "scalar":       _render_scalar,
        "vector":       _render_vector,
        "matrix":       _render_matrix,
        "matrix_group": _render_matrix_group,
        "table":        _render_table,
        "plot":         _render_plot,
        "error":        _render_error,
        "raw":          _render_raw,
    }
    fn = renderers.get(payload["type"], _render_raw)
    return fn(payload)


def _render_scalar(p):
    return html.Div(className="result-scalar", children=[
        html.Span(p["label"],          className="result-label"),
        html.Span(f'{p["value"]:.6g}', className="result-value"),
    ])


def _render_vector(p):
    return html.Div(className="result-vector", children=[
        html.Span(p["label"], className="result-label"),
        html.Ul([html.Li(f"{v:.6g}") for v in p["values"]]),
    ])


def _render_matrix(p):
    return html.Div(className="result-matrix", children=[
        html.Span(p["label"], className="result-label"),
        html.Table(html.Tbody([
            html.Tr([html.Td(f"{v:.6g}") for v in row])
            for row in p["values"]
        ])),
    ])


def _render_matrix_group(p):
    children = []
    for key in ["L", "U", "P"]:
        if key in p:
            children.append(_render_matrix({"label": key, "values": p[key]}))
    if "solution" in p:
        children.append(_render_vector({"label": "Solución", "values": p["solution"]}))
    return html.Div(children, className="result-matrix-group")


def _render_table(p):
    columns = [{"name": c, "id": c} for c in p["columns"]]
    data    = [dict(zip(p["columns"], row)) for row in p["rows"]]
    return dash_table.DataTable(
        columns=columns,
        data=data,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "right", "fontFamily": "monospace"},
        style_header={"fontWeight": "bold"},
    )


def _render_plot(p):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=p["x"],
        y=p["y"],
        mode="lines",
        name=p.get("label", "curva"),
    ))
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="x",
        yaxis_title="y",
    )
    return dcc.Graph(figure=fig, className="result-plot")


def _render_error(p):
    details = p.get("details") or {}
    children = [html.Strong("Error: "), html.Span(p["message"])]
    if details.get("error_type"):
        children.append(html.Pre(f'Tipo: {details["error_type"]}'))
    if details.get("context"):
        children.append(html.Pre(f'Contexto: {details["context"]}'))
    return html.Div(children, className="result-error")


def _render_raw(p):
    return html.Pre(str(p), className="result-raw")