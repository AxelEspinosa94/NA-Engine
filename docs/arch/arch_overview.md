# NA-Engine — Architecture Overview

## 1. Purpose

NA-Engine is a numerical analysis calculator built on a layered architecture that separates mathematical logic, input validation, execution, and UI rendering into independent, testable components. Each layer communicates through well-defined contracts, making it straightforward
to add new numerical methods without modifying existing infrastructure.

---

## 2. High-Level Flow

```
User Input (Dash UI)
        │
        ▼
<method>_callbacks.py
        │  builds input_data dict + calls NumericalMethod
        ▼
┌─────────────────────────────────────────────────────┐
│                   NumericalMethod                   │
│                   (base_method.py)                  │
│                                                     │
│  1. MethodRegistry.load_catalog()                   │
│       └── reads method_catalog.json                 │
│       └── resolves constructor / validator /        │
│           executor class paths                      │
│                                                     │
│  2. _load_class() × 3                               │
│       └── dynamic import via importlib              │
│                                                     │
│  3. validate_input()                                │
│       └── delegates to InterpolationValidator       │
│                                                     │
│  4. execute()                                       │
│       └── delegates to InterpolationExecutor        │
│       └── on failure → ErrorNormalizer.normalize()  │
└─────────────────────────────────────────────────────┘
        │
        │  outcome dict
        ▼
┌─────────────────────────────────────────────────────┐
│                    UIContract                       │
│                    (contract.py)                    │
│                                                     │
│  resolve(calculation_mode, outcome)                 │
│       ├── error path → Renderer.render_error()      │
│       └── success path → Renderer.render()          │
│               └── _build_blocks()                   │
│                     ├── _block_value()              │
│                     ├── _block_expression()         │
│                     ├── _block_plot()               │
│                     └── _block_table()              │
└─────────────────────────────────────────────────────┘
        │
        │  html.Div (tree of Dash components)
        ▼
Output("interp-result-area", "children")
        │
        ▼
    Browser
```

---

## 3. Layer Responsibilities

### 3.1 Catalog — `core/method_catalog.json`

Maps a method name to its three class paths:

```json
{
  "method": {
    "classConstructor": "core.<module>.<module>.<Module>",
    "classInputValidator": "strategies.validators.<module>_validators.<Module>Validator",
    "classExecutor": "strategies.executors.<module>_executors.<Module>Executor"
  }
}
```

Adding a new method requires only a new entry here — no changes to `NumericalMethod`. 
The catalog is loaded once and cached by `MethodRegistry`.

---

### 3.2 NumericalMethod — `core/base_method.py`

The central orchestrator. It:

- Loads the catalog via `MethodRegistry`
- Dynamically imports constructor, validator and executor classes via `importlib`
- Instantiates them and runs the pipeline: construct → validate → execute

It is **method-agnostic**: it does not know what interpolation or integration means, only that there is a constructor, a validator, and an executor to call in order.

**Output contract from `execute()`:**

```python
# Success
{
    "status":  "success",
    "result":  { ... },   # raw output from the executor
    "message": ""
}

# Error (normalized by ErrorNormalizer)
{
    "status":     "error",
    "error_type": "ValidationError | ExecutionError | ConstructionError | ...",
    "message":    "human-readable description",
    "context": {
        "method":     <"method">,
        "input_data": { ... }
    }
}
```

---

### 3.3 Constructor — e.g. `core/<module>/<module>`

Receives `input_data` and `**kwargs`. Responsible for:

- First-level validation (empty DataFrames, missing keys, invalid types)
- Storing parsed attributes (`self.df`, `self.xk`, `self.calculation_mode`, etc.)

Raises `ConstructionError` on failure.

---

### 3.4 Validator — `strategies/validators/<module>_validators.py`

Implements `ValidatorProtocol`:

```python
class ValidatorProtocol(Protocol):
    def validate(self, input_data: Dict[str, Any]) -> bool: ...
```

Responsible for method-specific validation, for 
example:

- Hermite: checks that the `dy` column is present
- Lagrange/Newton: checks minimum number of nodes
- Splines: checks that nodes are strictly increasing in `x`

Returns `True` or raises `ValidationError`.

---

### 3.5 Executor — `strategies/executors/<module>_executors.py`

Implements `ExecutorProtocol`:

```python
class ExecutorProtocol(Protocol):
    def run(self, instance: Any) -> Any: ...
```

`run()` dispatches to the correct private method based on `instance.calculation_mode`:

```python
def run(self, instance):
    dispatch = {
        "lagrange": self._run_lagrange,
        "newton":   self._run_newton,
        "splines":  self._run_spline,
        "hermite":  self._run_hermite,
    }
    return dispatch[instance.calculation_mode](instance)
```

Each `_run_*` method returns a dict with a consistent structure:

```python
{
    "value":      float,        # interpolated value at xk
    "expression": str,          # symbolic polynomial expression
    "table":      pd.DataFrame, # input nodes
    "x":          list[float],  # x points for plotting
    "y":          list[float],  # y points for plotting
    "x_nodes":    list[float],  # original x nodes
    "y_nodes":    list[float],  # original y nodes
}
```

---

### 3.6 ErrorNormalizer — `core/error_normalizer.py`

Maps Python exceptions to typed error strings:

| Exception          | `error_type`          |
|--------------------|-----------------------|
| `ValidationError`  | `"ValidationError"`   |
| `ExecutionError`   | `"ExecutionError"`    |
| `ConstructionError`| `"ConstructionError"` |
| `ZeroDivisionError`| `"MathError"`         |
| `SyntaxError`      | `"FunctionSyntaxError"`|
| `NameError`        | `"FunctionNameError"` |
| anything else      | `"InternalError"`     |

Always returns the standardized outcome dict described in §3.2.

---

### 3.7 Renderer — `core/renderer.py`

Converts the raw executor result dict into a typed payload dict.
Uses a two-step dispatch:

1. **Error detection** — if `"error"` key is present, routes to `render_error()`
2. **KEY_DISPATCH** — inspects result keys to determine payload type:

```python
KEY_DISPATCH = [
    ("derivative",       "scalar"),
    ("second_derivative","scalar"),
    ("third_derivative", "scalar"),
    ("inverse",          "matrix"),
    (("L", "U", "P"),   "matrix_group"),
    (("x", "y"),        "plot"),
    ("table",            "table"),
    ("markdown",         "markdown"),
    ("solution",         "vector"),
]
```

Output is always a typed dict: `{"type": "scalar|vector|matrix|plot|...", ...}`.
`Renderer` is **Dash-agnostic** — it only knows about data shapes, not components.

---

### 3.8 UIContract — `core/contract.py`

The bridge between `NumericalMethod.execute()` and the Dash UI.
Single public method: `resolve(calculation_mode, outcome) -> html.Div`.

Responsibilities:
- Routes error outcomes directly to `build_result_view()`
- For success, calls `Renderer.render()` then `_build_blocks()`
- `_build_blocks()` inspects the result keys and builds an ordered list of Dash components:

```
"value"      → _block_value()       Markdown with LaTeX boxed result
"expression" → _block_expression()  Markdown code block with polynomial
"x" + "y"   → _block_plot()        Plotly figure with curve + nodes
"table"      → _block_table()       DataTable with input nodes
```

Each block is independent — methods that return fewer keys produce fewer blocks
with no changes to the contract.

---

### 3.9 result_view — `app/components/result_view.py`

Converts a typed Renderer payload into concrete Dash components.
One private function per type: `_render_scalar`, `_render_vector`,
`_render_matrix`, `_render_matrix_group`, `_render_table`, `_render_plot`,
`_render_error`, `_render_raw`.

Used by `UIContract` for error payloads and as a fallback for unknown result types.

---

### 3.10 Callbacks — `app/callbacks/interpolation_callbacks.py`

Two callbacks per section:

| Callback | Trigger | Output |
|----------|---------|--------|
| `build_input_area` | method + input mode selected | dynamic form components |
| `run_interpolation` | Calcular button clicked | result area children |

`run_interpolation` is the only place where `NumericalMethod` and `UIContract` are
instantiated together. It handles `ValidationError` before calling `execute()` and
passes the outcome dict directly to `contract.resolve()`.

---

## 4. Project Structure (relevant paths)

```
NA-Engine/
├── core/
│   ├── base_method.py          # NumericalMethod orchestrator
│   ├── registry.py             # MethodRegistry + catalog cache
│   ├── method_catalog.json     # method → class path mapping
│   ├── exceptions.py           # typed exceptions
│   ├── error_normalizer.py     # exception → error dict
│   ├── renderer.py             # result dict → typed payload
│   └── contract.py             # outcome dict → html.Div
│
├── strategies/
│   ├── validators/
│   │   └── interpolation_validators.py
│   └── executors/
│       └── interpolation_executors.py
│
├── app/
│   ├── app.py                  # Dash app factory
│   ├── components/
│   │   └── result_view.py      # typed payload → Dash components
│   ├── layout/
│   │   └── interpolation_layout.py
│   └── callbacks/
│       └── interpolation_callbacks.py
│
└── tests/
    ├── unit/
    └── integration/
```

---

## 5. Extension Guide

To add a new numerical method (e.g. `"gauss"`):

1. **Catalog** — add entry to `method_catalog.json`
2. **Constructor** — create class in `core/<module>/`
3. **Validator** — add method-specific rules to the relevant validator
4. **Executor** — add `_run_gauss()` to the relevant executor, return the standard dict
5. **Layout** — add section in `app/layout/`
6. **Callbacks** — register in `app/callbacks/` and `app/app.py`

No changes needed to `NumericalMethod`, `Renderer`, `UIContract`, or `result_view`.