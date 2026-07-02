# Constructor Layer

## 1. Purpose

The constructor is the first layer invoked by `NumericalMethod` after loading the catalog.
Its responsibility is to receive `input_data`, parse it into typed class attributes, and perform a first-level sanity check to ensure the input is minimally valid and calculable.

It does **not** perform method-specific validation — that is the responsibility of the Validator layer. The division of concerns is:

| Layer       | Validates                                                      |
|-------------|----------------------------------------------------------------|
| Constructor | Input is present, non-empty, and structurally correct         |
| Validator   | Input is mathematically valid for the specific method         |

**Example:**

```
Constructor → xk is not None and not ""
Validator   → xk is within the interval defined by the DataFrame
```

---

## 2. Interface

All constructors share the same signature:

```python
class <Module>(self, input_data: Dict[str, Any], **kwargs: Any) -> None
```

`input_data` is a dictionary with variable keys depending on the domain.
`**kwargs` is currently only present in `Interpolation` and is reserved for future use across all modules.

`NumericalMethod` instantiates the constructor as:

```python
self.method_instance = self.constructor_class(self.input, **self.kwargs)
```

---

## 3. Responsibilities

### 3.1 Attribute assignment

The constructor unpacks `input_data` into typed class attributes:

```python
# Example: Interpolation
self.df                = input_data["data"]
self.xk                = input_data["xk"]
self.calculation_mode  = input_data["calculation_mode"]
self.mode              = input_data["mode"]  # "table" | "function" | "upload"
```

This makes the instance readable by the Executor without requiring it to know the structure of `input_data`.

### 3.2 DataFrame construction

When `mode == "function"`, the constructor generates the DataFrame from the symbolic expression rather than receiving it directly:

```python
if self.mode == "function":
    self.df = self._build_dataframe_from_function(
        expr=input_data["expression"],
        a=input_data["a"],
        b=input_data["b"],
        n=input_data["n"],
    )
```

When `mode == "table"` or `mode == "upload"`, `input_data["data"]` is already a DataFrame and is assigned directly.

### 3.3 First-level validation

The constructor raises `ConstructionError` when the input is structurally invalid, regardless of the method being used. Typical checks:

- `xk` is not `None` or empty string
- `data` is not an empty DataFrame
- Required keys are present in `input_data`

For `Interpolation` with `calculation_mode == "hermite"`, the constructor also checks that the DataFrame has exactly 3 columns (`x`, `y`, `dy`), since this is a
structural requirement that applies before any mathematical validation can occur.

On failure, raises:

```python
raise ConstructionError("Descriptive message")
```

Which is caught by `NumericalMethod` and normalized by `ErrorNormalizer` into:

```python
{
    "status":     "error",
    "error_type": "ConstructionError",
    "message":    "...",
    "context":    { ... }
}
```

---

## 4. Existing Constructors

| Module          | Class                | File                                        | kwargs |
|-----------------|----------------------|---------------------------------------------|--------|
| Interpolation   | `Interpolation`      | `core/interpolation/interpolation.py`       | yes    |
| Integration     | `Integration`        | `core/integration/integral.py`              | no*    |
| ODE             | `ODE`                | `core/ode/ODE.py`                              | no*    |
| Linear Algebra             | `linearAlgebra`                | `core/ode/linearAlgebra/linear-algebra.py`                              | no*    |
| Non-Linear Equation             | `NonLinearEquation`                | `core/nonlinear/Non-linear-base.py`                              | no*    |
| Numerical Derivative             | `NumericalDerivative`                | `core/derivative/numerical_derivative.py`                              | no*    |

*`**kwargs` support is planned for future modules.

---

## 5. What the Constructor Does NOT Do

- It does not dispatch to a specific numerical method — that is the Executor's job.
- It does not perform mathematical validation (interval checks, singularity detection, minimum node counts) — that is the Validator's job.
- It does not format or render output — that is the Renderer and UIContract's job.

---

## 6. Extension Guide

When adding a new module:

1. Create the class in `core/<module>/<module>.py`
2. Accept `input_data: Dict[str, Any]` and `**kwargs` (even if unused, for consistency)
3. Assign all relevant attributes from `input_data`
4. Handle `mode`-based DataFrame construction if applicable
5. Raise `ConstructionError` for structurally invalid inputs
6. Register the class path in `method_catalog.json`

```json
{
  "<method>": {
    "classConstructor": "core.<module>.<module>.<Module>",
    ...
  }
}
```