# Validator Layer

## 1. Purpose

The Validator performs method-specific mathematical validation after the Constructor has parsed and structured `input_data`. It answers the question: **is this input mathematically valid for the requested calculation mode?**

It does not check structural integrity (missing keys, empty DataFrames, wrong types) — that is the Constructor's responsibility. The division of concerns is:

| Layer       | Validates                                                      |
|-------------|----------------------------------------------------------------|
| Constructor | Input is present, non-empty, and structurally correct         |
| Validator   | Input is mathematically valid for the specific method         |

**Example for Interpolation:**

```
Constructor → xk is not None and not ""
Validator   → xk is within the interval [x_min, x_max] of the DataFrame
```

---

## 2. Interface

All validators implement `ValidatorProtocol`:

```python
class ValidatorProtocol(Protocol):
    def validate(self, input_data: Dict[str, Any]) -> bool: ...
```

`NumericalMethod` calls it as:

```python
is_valid = self.validator.validate(self.input)
```

Where `self.input` is the original `input_data` dict — not the constructor instance.
The validator receives the same dict the constructor received, including any keys added or enriched during construction (e.g. a DataFrame built from a function expression).

Returns `True` on success. Raises `ValidationError` on failure — never returns `False` silently, as `NumericalMethod.validate_input()` treats a `False` return as a `ValidationError` regardless.

---

## 3. Internal Structure

### 3.1 General pattern: dispatcher by `calculation_mode`

Since most domains have multiple calculation modes with different validation requirements,
each validator uses an internal dispatcher to route to the correct validation function:

```python
class <Module>Validator:
    def validate(self, input_data: Dict[str, Any]) -> bool:
        mode = input_data.get("calculation_mode")
        dispatch = {
            "method_a": self._validate_method_a,
            "method_b": self._validate_method_b,
        }
        fn = dispatch.get(mode)
        if fn is None:
            raise ValidationError(f"Unknown calculation_mode: '{mode}'")
        return fn(input_data)

    def _validate_method_a(self, input_data): ...
    def _validate_method_b(self, input_data): ...
```

Each `_validate_*` function is independent and contains only the rules relevant to that mode. Functions are not overloaded because the validation rules are typically
different enough that sharing logic would introduce unnecessary coupling.

### 3.2 Exception: Interpolation

Interpolation breaks the dispatcher pattern because Lagrange, Newton, and Splines share the same input structure (`df`, `xk`) and therefore the same validation rules.
A single `_validate_default` function handles all three, and only Hermite gets its own branch:

```python
class InterpolationValidator:
    def validate(self, input_data: Dict[str, Any]) -> bool:
        mode = input_data.get("calculation_mode")
        if mode == "hermite":
            return self._validate_hermite(input_data)
        return self._validate_default(input_data)
```

**`_validate_default`** (Lagrange, Newton, Splines):
- DataFrame has at least 2 nodes
- No `NaN` values in `x` or `y`
- `x` values are strictly increasing
- `xk` is within `[x_min, x_max]`

**`_validate_hermite`** (Hermite):
- All checks from `_validate_default`
- DataFrame has exactly 3 columns (`x`, `y`, `dy`)
- No `NaN` values in the `dy` column

---

## 4. Existing Validators

| Module        | Class                      | File                                                  |
|---------------|----------------------------|-------------------------------------------------------|
| Interpolation | `InterpolationValidator`   | `strategies/validators/interpolation_validators.py`   |
| Integration   | `IntegrationValidator`     | `strategies/validators/integration_validators.py`     |
| ODE           | `ODEValidator`             | `strategies/validators/ode_validators.py`             |
| Linear Algebra           | `Linear-AlgebraValidator`             | `strategies/validators/linear-algebra-validators.py`             |
| Non-Linear           | `Non-LinearValidator`             | `strategies/validators/Non-linear-validators.py`             |
| Numerical Derivative           | `NumericalDerivativeValidator`             | `strategies/validators/numerical-derivative-validators.py`             |

---

## 5. Error Handling

Validators raise `ValidationError` with a human-readable message:

```python
raise ValidationError("xk must be within the interpolation interval [x_min, x_max].")
```

`NumericalMethod.validate_input()` catches `ValidationError` and re-raises it.
The callback layer catches it before calling `execute()` and passes it directly to `UIContract.resolve()` as a structured error outcome:

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

## 6. What the Validator Does NOT Do

- It does not parse or transform input — attributes are already set by the Constructor.
- It does not execute the numerical method or inspect results.
- It does not render error messages — that is `UIContract`'s responsibility.
- It does not return descriptive payloads — only `True` or raises `ValidationError`.

---

## 7. Extension Guide

When adding a new module or calculation mode:

1. Create `strategies/validators/<module>_validators.py`
2. Define `class <Module>Validator` with a single `validate()` method
3. Add an internal dispatcher if the module has multiple calculation modes
4. Add a dedicated `_validate_<mode>()` function per mode
5. Reuse a shared `_validate_default()` if modes share the same rules
6. Raise `ValidationError` with descriptive messages — never return `False` silently
7. Register the class path in `method_catalog.json`

```json
{
  "<method>": {
    "classInputValidator": "strategies.validators.<module>_validators.<Module>Validator",
    ...
  }
}
```