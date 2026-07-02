# Renderer Layer

## 1. Purpose

The Renderer transforms the raw result dict returned by the Executor into a standardized, typed payload dict. It is the bridge between mathematical output and visual representation — but it is **Dash-agnostic**: it knows nothing about components, callbacks, or the UI framework.

Its single responsibility is: **given a result dict, determine its type and normalize it into a consistent payload structure.**

---

## 2. Interface

```python
class Renderer:
    def render(self, calculation_mode: str, result: Dict[str, Any]) -> Dict[str, Any]:
```

Called by `UIContract.resolve()` as:

```python
payload = self.renderer.render(calculation_mode, result)
```

Where:
- `calculation_mode` is the method string (e.g. `"lagrange"`, `"rk4"`). Currently unused internally but kept for future extensibility.
- `result` is the raw dict from the Executor, or an error dict from `ErrorNormalizer`.

Returns a typed payload dict always containing at minimum a `"type"` key.

---

## 3. Dispatch Mechanism

`render()` uses a two-level dispatch:

### Level 1 — Error detection (priority)

If `"error"` is present in `result`, routes immediately to `render_error()` regardless of any other keys:

```python
if "error" in result:
    return self.render_error(result)
```

### Level 2 — KEY_DISPATCH

Inspects the keys present in `result` to determine the payload type:

```python
KEY_DISPATCH: List[Tuple[Union[str, Tuple[str, ...]], str]] = [
    ("derivative",        "scalar"),
    ("second_derivative", "scalar"),
    ("third_derivative",  "scalar"),
    ("inverse",           "matrix"),
    (("L", "U", "P"),    "matrix_group"),
    (("x", "y"),         "plot"),
    ("table",             "table"),
    ("markdown",          "markdown"),
    ("solution",          "vector"),
]
```

Rules are evaluated in order. Each entry is:
- `str` → single key must be present in result
- `tuple` → **all** keys in the tuple must be present

The first matching rule determines the renderer type. If no rule matches, falls back to `{"type": "raw", "data": result}`.

---

## 4. Payload Types

Each renderer method produces a typed dict consumed by `UIContract` and `result_view`:

### `scalar`
```python
{"type": "scalar", "label": str, "value": float}
```

### `vector`
```python
{"type": "vector", "label": str, "values": list[float]}
```

### `matrix`
```python
{"type": "matrix", "label": str, "values": list[list[float]]}
```

### `matrix_group`
```python
{"type": "matrix_group", "L": list, "U": list, "P": list, "solution": list[float]}
```

### `plot`
```python
{"type": "plot", "label": str, "x": list[float], "y": list[float]}
```

### `table`
```python
{"type": "table", "columns": list[str], "rows": list[list]}
```

### `markdown`
```python
{"type": "markdown", "content": str}
```

### `error`
```python
{"type": "error", "message": str, "details": dict | None}
```

### `raw` (fallback)
```python
{"type": "raw", "data": dict}
```

---

## 5. Design Decisions

**Renderer is Dash-agnostic.** It only produces plain Python dicts. This makes it independently testable without a running Dash instance and reusable if the frontend framework changes.

**KEY_DISPATCH order matters.** Rules are evaluated top to bottom and the first match wins. If a result dict contains both `"solution"` and `"x"/"y"`, the `plot`
rule takes priority because it appears first. When adding new rules, consider the order carefully to avoid unintended matches.

**Interpolation results bypass Renderer for most keys.** Results from the Interpolation executor (`value`, `expression`, `table`, `x`, `y`, `x_nodes`,
`y_nodes`) are handled directly by `UIContract._build_blocks()` rather than routed through `KEY_DISPATCH`. The Renderer is still called for error payloads and as a fallback, but the block-building logic lives in `UIContract` for composite results that require multiple visual components.

---

## 6. What the Renderer Does NOT Do

- It does not create Dash components — that is `result_view.py`'s responsibility.
- It does not generate explanations or markdown content — that is `UIContract`'s responsibility.
- It does not know about `calculation_mode` beyond accepting it as a parameter.
- It does not handle composite results (multiple visual blocks) — that is `UIContract._build_blocks()`'s responsibility.

---

## 7. Extension Guide

To support a new result key or type:

1. Add a new entry to `KEY_DISPATCH` in the correct position (order matters):
```python
("new_key", "new_type"),
```

2. Add the corresponding renderer method:
```python
def render_new_type(self, value: Any, label: str = "value") -> Dict[str, Any]:
    return {
        "type":  "new_type",
        "label": label,
        "data":  ...,
    }
```

3. Register it in the `type_dispatch` dict inside `render()`:
```python
type_dispatch = {
    ...
    "new_type": self.render_new_type,
}
```

4. Add the corresponding visual renderer in `result_view.py`:
```python
def _render_new_type(p):
    return html.Div(...)
```