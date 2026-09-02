
---

# **Validator Layer Documentation**


# **Table of Contents**

-   [Purpose](#1-purpose)
    -   [Division of Responsibilities](#division-of-responsibilities) 
-   [Interface](#2-interface)
-   [Internal Structure](#3-internal-structure)
    -   [General Pattern Dispatcher by Calculation Mode](#31-general-pattern-dispatcher-by-calculation_mode)
    -   [Exception - Interpolation Module](#32-exception-interpolation)
-   [Existing Validators](#4-existing-validators)
-   [Validation Catalog Philosophy](#5-validation-catalog-philosophy-json)
    -   [Design Philosophy](#design-philosophy)
-   [Rule Subscripts](#6-rule-subscripts)
-   [Error Handling](#7-error-handling)
-   [What Validators Do Not Do](#8-what-validators-do-not-do)
-   [Extension Guide](#9-extension-guide)
-   [Summary](#10-summary)

## **1. Purpose**

The Validator performs **method‑specific mathematical validation** after the Constructor has parsed and structured `input_data`.

It answers the question:

> **Is this input mathematically valid for the requested calculation mode?**

It does **not** check structural integrity (missing keys, empty DataFrames, wrong types).  
That is the Constructor’s responsibility.

### **Division of Responsibilities**

| Layer        | Validates                                                        |
|--------------|------------------------------------------------------------------|
| Constructor  | Input is present, non‑empty, and structurally correct            |
| Validator    | Input is mathematically valid for the specific numerical method  |

**Example (Interpolation):**

```
Constructor → xk is not None and not ""
Validator   → xk lies within the interval [x_min, x_max] of the DataFrame
```

---

## **2. Interface**

All validators implement `ValidatorProtocol`:

```python
class ValidatorProtocol(Protocol):
    def validate(self, input_data: Dict[str, Any]) -> bool: ...
```

`NumericalMethod` calls it as:

```python
is_valid = self.validator.validate(self.input)
```

Where `self.input` is the original `input_data` dictionary — not the constructor instance.

The validator receives the same dict the constructor received, including any keys added or enriched during construction (e.g., a DataFrame built from a function expression).

Validators return `True` on success.  
They raise `ValidationError` on failure — never return `False` silently.

---

## **3. Internal Structure**

### **3.1 General Pattern: Dispatcher by `calculation_mode`**

Most modules contain multiple calculation modes with different validation rules.  
Therefore, each validator uses an internal dispatcher:

```python
class <Module>Validator:
    def validate(self, input_data):
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

Each `_validate_*` function is independent and contains only the rules relevant to that mode.

### **3.2 Exception: Interpolation**

Interpolation breaks the dispatcher pattern because Lagrange, Newton, and Splines share the same input structure (`df`, `xk`) and therefore the same validation rules.

Only Hermite requires its own branch:

```python
class InterpolationValidator:
    def validate(self, input_data):
        mode = input_data.get("calculation_mode")
        if mode == "hermite":
            return self._validate_hermite(input_data)
        return self._validate_default(input_data)
```

**`_validate_default`** (Lagrange, Newton, Splines):

- DataFrame has at least 2 nodes  
- No `NaN` values in `x` or `y`  
- `x` values strictly increasing  
- `xk` lies within `[x_min, x_max]`

**`_validate_hermite`** (Hermite):

- All checks from `_validate_default`  
- DataFrame has exactly 3 columns (`x`, `y`, `dy`)  
- No `NaN` values in the `dy` column  

---

## **4. Existing Validators**

| Module            | Class                          | File Path                                                      |
|-------------------|--------------------------------|----------------------------------------------------------------|
| Interpolation     | `InterpolationValidator`       | `strategies/validators/interpolation_validators.py`            |
| Integration       | `IntegrationValidator`         | `strategies/validators/integration/integration_validators.py`  |
| ODE               | `ODEValidator`                 | `strategies/validators/ode_validators.py`                      |
| Linear Algebra    | `LinearAlgebraValidator`       | `strategies/validators/linear_algebra_validators.py`           |
| Non‑Linear        | `NonLinearValidator`           | `strategies/validators/non_linear_validators.py`               |
| Numerical Deriv.  | `NumericalDerivativeValidator` | `strategies/validators/numerical_derivative_validators.py`     |

---

## **5. Validation Catalog Philosophy (JSON)**

Each module includes a JSON catalog (e.g., `integration_validation_catalog.json`) that defines:

- **SUPPORTED_MODES** → the authoritative list of valid calculation modes  
- **rules** → paths to sub‑scripts implementing validation logic  
- **metadata** → optional UI or documentation hints  

Example:

```json
{
  "supported_modes": [
    "trapezoid_simple",
    "trapezoid_composite",
    "simpson_1_3",
    "simpson_3_8",
    "romberg",
    "gauss",
    "<new-method>"
  ],
  "clenshaw_curtis": {
    "rules": "strategies.validators.integration.rules.<new-method>.<validation-function>"
  }
}
```

### **Design Philosophy**

1. **The catalog is the single source of truth**  
   Validators should not hardcode lists of modes.

2. **Each method may have its own rule file**  
   Example:  
   `strategies/validators/integration/rules/clenshaw.py`

3. **Scalable architecture**  
   Adding a new method does not require modifying the validator class — only the JSON and the rule file.

4. **Decoupled logic**  
   The validator simply dispatches to the rule defined in the catalog.

---

## **6. Rule Sub‑scripts**

To keep validators clean, each method can define its own rule file:

```
strategies/
  validators/
    integration/
      rules/
        common_rules.py
        gauss.py
        <new-method>.py
```

Example rule:

```python
def validate_clenshaw(input_data):
    n = input_data.get("n")
    if n % 2 != 0:
        raise ValidationError("Clenshaw-Curtis requires even n.")
    return True
```

The validator simply imports and calls it.

---

## **7. Error Handling**

Validators raise `ValidationError` with a human‑readable message:

```python
raise ValidationError("xk must lie within the interpolation interval [x_min, x_max].")
```

`NumericalMethod.validate_input()` catches the exception and forwards it to `UIContract.resolve()`:

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

## **8. What Validators Do NOT Do**

- They do **not** parse or transform input  
- They do **not** execute numerical methods  
- They do **not** render UI messages  
- They do **not** return payloads — only `True` or raise `ValidationError`

---

## **9. Extension Guide**

When adding a new module:

**1. Create a folder following the Integration module structure**

Recommended layout:

```
strategies/
  validators/
    <module>/
      __init__.py
      <module>_validators.py
      <module>_validation_catalog.json
      rules/
        __init__.py
        common_rules.py
        <method>.py
```

**2. Register the validator in `method_catalog.json`**

```json
{
  "<method>": {
    "classInputValidator": "strategies.validators.<module>.<module>_validators.<ModuleValidator>",
    ...
  }
}
```

**3. Add the new method to `SUPPORTED_MODES`**

Always append it at the end:

```json
"supported_modes": [
  "trapezoid_simple",
  "trapezoid_composite",
  "simpson_1_3",
  "simpson_3_8",
  "romberg",
  "gauss",
  "clenshaw_curtis",
  "<new-method>"
]
```

**4. Create a rule file for the new method**

Example:

```
strategies/validators/integration/rules/<new-method>.py
```

**5. Add the rule path in the catalog**

```json
"<new-method>": {
  "rules": "strategies.validators.integration.rules.<new-method>.<validation_function>"
}
```

**6. Implement `_validate_<new-method>()` or use the rule file**

**7. Always raise `ValidationError` with a clear message**

---

## **10. Summary**

The Validator Layer is now:

- modular  
- scalable  
- catalog‑driven  
- cleanly separated from construction and execution  
- easy to extend with new modules and methods  
- consistent with NA‑Engine’s architecture  

---
