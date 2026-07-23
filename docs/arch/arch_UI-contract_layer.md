# UIContract Layer

## 1. Purpose

`UIContract` is the bridge between `NumericalMethod.execute()` and the Dash UI.
It receives the raw outcome dict from the executor pipeline, routes it through `Renderer`, and returns a fully composed `html.Div` tree ready to be assigned to a Dash `Output`.

It is the only layer that knows both the shape of the backend outcome dict **and** how to build Dash components from it.

---

## 2. Interface

```python
class UIContract:
    def __init__(self, renderer: Renderer | None = None) -> None:
        self.renderer = renderer or Renderer()

    def resolve(self, calculation_mode: str, outcome: Dict[str, Any]) -> html.Div:
```

Instantiated once per callbacks module as a global:

```python
# app/callbacks/interpolation_callbacks.py
contract = UIContract()
```

Called inside each execution callback:

```python
outcome = nm.execute()
return contract.resolve(method, outcome)
```

---

## 3. Outcome Dict Contract

`resolve()` expects the standardized outcome dict produced by `NumericalMethod.execute()` or constructed manually by the callback on validation failure:

**Success:**
```python
{
    "status":  "success",
    "result":  { ... },  # raw executor output
    "message": str,      # optional, empty string if not set
}
```

**Error:**
```python
{
    "status":     "error",
    "error_type": str,   # normalized by ErrorNormalizer
    "message":    str,   # human-readable description
    "context":    dict,  # method name + input_data
}
```

The callback layer is responsible for constructing the error dict when `ValidationError` is raised before `execute()` is called:

```python
try:
    nm.validate_input()
except ValidationError as e:
    return contract.resolve(method, {
        "status":     "error",
        "error_type": "ValidationError",
        "message":    str(e),
        "context":    input_data,
    })
```

---

## 4. Internal Flow

```
resolve(calculation_mode, outcome)
        │
        ├── status == "error"
        │       └── renderer.render(mode, {"error": message, "details": context})
        │               └── build_result_view(error_payload)
        │                       └── html.Div (error block)
        │
        └── status == "success"
                └── result = outcome["result"]
                        └── _build_blocks(calculation_mode, result)
                                ├── "value"      → _block_value()
                                ├── "expression" → _block_expression()
                                ├── "x" + "y"   → _block_plot()
                                └── "table"      → _block_table()
                                        └── html.Div (ordered blocks)
```

---

## 5. `_build_blocks()`

Inspects the keys present in `result` and builds an ordered list of Dash components.
Each key maps to an independent visual block:

```python
def _build_blocks(self, calculation_mode: str, result: Dict[str, Any]) -> list:
    blocks = []

    if "value"      in result: blocks.append(self._block_value(calculation_mode, result))
    if "expression" in result: blocks.append(self._block_expression(result["expression"]))
    if "x" in result and "y" in result: blocks.append(self._block_plot(result))
    if "table"      in result: blocks.append(self._block_table(result["table"]))

    if not blocks:
        payload = self.renderer.render(calculation_mode, result)
        blocks.append(build_result_view(payload))

    return blocks
```

**Block order is intentional:**

```
1. value       → numerical result first, most important
2. expression  → symbolic representation of the method
3. plot        → visual curve with original nodes
4. table       → raw input nodes for reference
```

Methods that return fewer keys produce fewer blocks automatically — no changes to `_build_blocks()` are needed when a method omits optional keys.

**Fallback:** if no known keys are present, `_build_blocks()` delegates to `Renderer.render()` + `build_result_view()`, which handles scalar, vector, matrix, and other generic types via `KEY_DISPATCH`.

---

## 6. Block Builders

Each `_block_*` method receives the relevant slice of `result` and returns an `html.Div` with a descriptive markdown header and its visual component:

| Method               | Input                        | Output                              |
|----------------------|------------------------------|-------------------------------------|
| `_block_value()`     | `result["value"]`, mode      | `dcc.Markdown` with LaTeX `\boxed`  |
| `_block_expression()`| `result["expression"]`       | `dcc.Markdown` code block           |
| `_block_plot()`      | `result["x/y/x_nodes/y_nodes"]` | `dcc.Graph` (Plotly Scatter)     |
| `_block_table()`     | `result["table"]` (DataFrame)| `dcc.Markdown` header + `DataTable` |

`_block_plot()` renders two traces:
- **Curve** — polynomial/spline evaluated at 200 points (`x`, `y`)
- **Nodes** — original input points (`x_nodes`, `y_nodes`) as markers

---

## 7. Relationship with Renderer

`UIContract` and `Renderer` have complementary but distinct roles:

| Concern                        | Renderer         | UIContract             |
|--------------------------------|------------------|------------------------|
| Knows outcome dict shape       | No               | Yes                    |
| Knows Dash components          | No               | Yes                    |
| Handles composite results      | No               | Yes (`_build_blocks`)  |
| Handles generic typed payloads | Yes (KEY_DISPATCH)| No (delegates)        |
| Testable without Dash          | Yes              | No                     |

For **composite results** (interpolation: value + expression + plot + table), `UIContract` bypasses `KEY_DISPATCH` entirely and builds blocks directly.

For **generic results** (scalar, vector, matrix, matrix_group from other modules), `UIContract` delegates to `Renderer.render()` + `build_result_view()` via the
`_build_blocks()` fallback.

---

## 8. Current State by Module

| Module        | Executor output  | `_build_blocks()` support | UI connected |
|---------------|------------------|---------------------------|--------------|
| Interpolation | value + expression + plot + table | Full | Yes |
| Integration   | TBD              | Via fallback (Renderer)   | Pending      |
| ODE           | TBD              | Via fallback (Renderer)   | Pending      |

When integration and ODE are connected to the UI, `_build_blocks()` may be extended with new branches if their result structures require composite layouts.
If their executor output maps cleanly to a single `KEY_DISPATCH` type (e.g. a scalar or a plot), the fallback handles them without any changes to `UIContract`.

---

## 9. What UIContract Does NOT Do

- It does not perform validation or mathematical computation.
- It does not call `NumericalMethod` — that is the callback's responsibility.
- It does not know about specific numerical methods by name.
- It does not store state between calls — each `resolve()` call is stateless.

---

## 10. Extension Guide

To support a new result key in `_build_blocks()`:

```python
if "new_key" in result:
    blocks.append(self._block_new_key(result["new_key"]))

def _block_new_key(self, data) -> html.Div:
    return html.Div([
        dcc.Markdown("### New Section", className="result-explanation"),
        ...
    ])
```

To connect a new module to the UI:

1. Instantiate `UIContract` as a global in the new callbacks file
2. Call `contract.resolve(calculation_mode, outcome)` inside the execution callback
3. If the executor result has a composite structure, add branches to `_build_blocks()`
4. If it maps to a single generic type, the fallback handles it automatically