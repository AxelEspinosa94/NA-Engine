# result_view Layer

## 1. Purpose

`result_view.py` is the final rendering layer. It converts a typed payload dict produced by `Renderer` into concrete Dash components (`html`, `dcc`, `dash_table`)
ready to be placed in the UI.

It is the only layer that knows about Dash component types. All upstream layers are framework-agnostic — `result_view.py` is where the framework dependency lives.

---

## 2. Interface

Single public function:

```python
def build_result_view(payload: dict) -> html.Div:
```

Called by `UIContract` in two scenarios:

1. **Error path** — directly after `Renderer.render_error()`:
```python
return build_result_view(error_payload)
```

2. **Fallback path** — inside `_build_blocks()` when no known composite key is present:
```python
payload = self.renderer.render(calculation_mode, result)
blocks.append(build_result_view(payload))
```

---

## 3. Internal Structure

`build_result_view()` uses an internal dispatcher keyed by `payload["type"]`:

```python
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
```

If `payload["type"]` is not recognized, falls back to `_render_raw` which renders the dict as a `<pre>` block for debugging.

---

## 4. Renderers by Type

### `scalar`
Displays a label and a numeric value side by side:
```
[label]  [value]
```
CSS classes: `result-scalar`, `result-label`, `result-value`

### `vector`
Displays a label followed by an unordered list of float values:
```
[label]
  • v1
  • v2
  • ...
```
CSS class: `result-vector`

### `matrix`
Displays a label followed by an HTML table with float-formatted cells:
```
[label]
┌           ┐
│ a00  a01  │
│ a10  a11  │
└           ┘
```
CSS class: `result-matrix`

### `matrix_group`
Renders L, U, P matrices sequentially using `_render_matrix()`, followed by the solution vector using `_render_vector()` if present:
```
[L matrix]
[U matrix]
[P matrix]
[solution vector]
```
CSS class: `result-matrix-group`

### `table`
Renders a `dash_table.DataTable` with right-aligned monospace cells:
```python
dash_table.DataTable(
    columns=[{"name": c, "id": c} for c in p["columns"]],
    data=[dict(zip(p["columns"], row)) for row in p["rows"]],
    style_cell={"textAlign": "right", "fontFamily": "monospace"},
)
```

### `plot`
Renders a `dcc.Graph` with a Plotly `Scatter` trace in `lines` mode:
```python
fig.add_trace(go.Scatter(x=p["x"], y=p["y"], mode="lines", name=p["label"]))
```
CSS class: `result-plot`

### `error`
Renders a styled error block with the message and optional details:
```
Error: [message]
Tipo: [error_type]     (if present)
Contexto: [context]    (if present)
```
CSS class: `result-error`

### `raw` (fallback)
Renders the full payload dict as a `<pre>` block for debugging unknown types:
```python
html.Pre(str(p), className="result-raw")
```

---

## 5. Design Decisions

**One function per type, no classes.** Each `_render_*` is a private module-level function. There is no shared state between renderers, so classes would add indirection without benefit.

**`_render_matrix_group` reuses `_render_matrix` and `_render_vector`.** Internal
reuse between renderers is acceptable because they operate on the same payload structure and are in the same module.

**`result_view` does not generate explanations or headers.** Markdown headers
and explanatory text are `UIContract._block_*`'s responsibility. `result_view` only renders the data component itself.

**Plotly theme is set to `plotly_dark` by default.** This aligns with the dark theme of the application. If light theme support for plots is needed in the future, the theme can be passed as a key in the payload.

---

## 6. Relationship with UIContract

`result_view` and `UIContract` have complementary roles:

| Concern                         | UIContract           | result_view             |
|---------------------------------|----------------------|-------------------------|
| Knows outcome dict shape        | Yes                  | No                      |
| Knows payload type structure    | Partially (fallback) | Yes (all types)         |
| Builds composite layouts        | Yes (`_build_blocks`)| No                      |
| Builds individual components    | No                   | Yes (`_render_*`)       |
| Generates explanatory markdown  | Yes (`_block_*`)     | No                      |
| Handles error payloads          | Routes to here       | Yes (`_render_error`)   |

---

## 7. What result_view Does NOT Do

- It does not call `Renderer` or `UIContract` — it only consumes typed payloads.
- It does not generate explanatory text or markdown headers.
- It does not know about `calculation_mode` or method names.
- It does not handle composite results (value + expression + plot + table) — that is `UIContract._build_blocks()`'s responsibility.
- It does not apply business logic — if a value is `NaN` or infinite, it renders it as-is without correction.

---

## 8. Extension Guide

To support a new payload type:

1. Add the renderer function:
```python
def _render_new_type(p: dict) -> html.Div:
    return html.Div([
        ...
    ], className="result-new-type")
```

2. Register it in the dispatcher inside `build_result_view()`:
```python
renderers = {
    ...
    "new_type": _render_new_type,
}
```

3. Add the corresponding CSS in `app/assets/interpolation.css`
   (or a dedicated module CSS file):
```css
.result-new-type {
    ...
}

#app-container.dark .result-new-type {
    ...
}
```

4. Ensure `Renderer` produces `{"type": "new_type", ...}` via `KEY_DISPATCH`
   or that `UIContract._build_blocks()` passes the correct payload structure.