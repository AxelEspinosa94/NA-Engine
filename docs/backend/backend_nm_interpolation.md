
---

# 📘 **Backend Documentation — Interpolation Module**

# NA‑Engine — Interpolation Module (Backend Documentation)

This document describes the backend implementation of the unified interpolation module in NA‑Engine.  
It covers the constructor, validator, executor, and an example calculation for each interpolation mode.

Supported modes:

- `lagrange`
- `newton`
- `spline_cubic`
- `hermite`

---

# I. Constructor (`Interpolation`)

The constructor is responsible for:

- Reading and storing user input  
- Building the internal DataFrame (`df`)  
- Handling both `"table"` and `"function"` modes  
- Preparing special structures for Hermite interpolation  

## 1. Standard interpolation (Lagrange, Newton, Spline)

When `calculation_mode` is **not** `"hermite"`:

- `"table"` mode expects a DataFrame with 2 columns:  
  `x`, `f(x)`
- `"function"` mode builds a DataFrame automatically using:
  - `data`: function string
  - `interval`: `[a, b]`
  - `step`: sampling step

## 2. Hermite interpolation

Hermite requires:

- `"table"` mode: DataFrame with **3 columns**  
  `x`, `f(x)`, `f'(x)`
- `"function"` mode:
  - `function`: function string  
  - `interval`: `[a, b]`  
  - `step`: sampling step  
  - The constructor computes `f'(x)` automatically using SymPy

The constructor ensures:

- Strictly increasing `x` values  
- No missing values  
- Correct number of columns  
- Proper DataFrame sorting  

---

# II. Validator (`InterpolationValidator`)

The validator performs input validation **before** the constructor runs.

It checks:

## 1. Mode
- Must be `"table"` or `"function"`

## 2. Table mode
### Lagrange / Newton / Spline:
- DataFrame with **2 columns**
- No NaN values
- Numeric types
- Strictly increasing `x`

### Hermite:
- DataFrame with **3 columns**
- No NaN values
- Numeric types
- Strictly increasing `x`
- At least 2 points

## 3. Function mode
- Function must be a string
- Interval must be `[a, b]` with `a < b`
- Step must be positive
- Hermite uses `"function"` instead of `"data"`

## 4. xk
- Must exist
- Must be numeric

If any rule fails, a `ValidationError` is raised.

---

# III. Executor (`InterpolationExecutor`)

The executor dispatches to one of four internal algorithms:

```python
{
  "lagrange": _run_lagrange,
  "newton": _run_newton,
  "spline_cubic": _run_spline,
  "hermite": _run_hermite
}
```

Each method returns a dictionary containing:

- `"value"`: interpolated value at `xk`
- `"table"`: the DataFrame used
- Additional method‑specific data

## 1. Lagrange
- Computes Lagrange basis polynomials \( L_i(x) \)
- Returns:
  - `"value"`
  - `"expression"` (symbolic string)
  - `"table"`

## 2. Newton
- Computes divided differences in‑place
- Evaluates Newton polynomial
- Returns:
  - `"value"`
  - `"coefficients"`
  - `"table"`

## 3. Cubic Spline
- Builds tridiagonal system for second derivatives \( M \)
- Solves using NumPy
- Evaluates spline segment containing `xk`
- Returns:
  - `"value"`
  - `"M"`
  - `"table"`

## 4. Hermite
- Builds duplicated nodes array `z`
- Builds divided differences matrix `Q`
- Evaluates Hermite polynomial in Newton form
- Returns:
  - `"value"`
  - `"z"`
  - `"Q"`
  - `"table"`

---

# IV. Example Calculation (Hermite)

Below is a complete example using Hermite interpolation.

```python
import pandas as pd
from core.base_method import NumericalMethod

df = pd.DataFrame({
    "x": [0, 1],
    "f(x)": [1, 2],
    "f'(x)": [0, 1]
})

method = NumericalMethod(
    method="interpolation",
    input_data={
        "mode": "table",
        "calculation_mode": "hermite",
        "data": df,
        "xk": 0.5
    }
)

method.validate_input()
result = method.execute()
```

### Expected Output

- The Hermite polynomial built from the table evaluates to approximately:

```
H(0.5) ≈ 1.375
```

### Example Result Structure

```json
{
  "status": "success",
  "result": {
    "value": 1.375,
    "z": [...],
    "Q": [...],
    "table": [...]
  }
}
```

---

# End of Document

---
