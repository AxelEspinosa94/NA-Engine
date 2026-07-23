
---

# NA‑Engine — Numerical Derivative Module (Backend Documentation)

This document describes the backend implementation of the Numerical Derivative module in NA‑Engine.  
It covers the constructor, validator, executor, and an example calculation for the supported derivative modes.

Supported calculation modes:

- `forward`
- `backward`
- `central`
- `richardson`
- `second_forward`
- `second_central`
- `third_forward`
- `partial_x`
- `partial_y`

All methods operate in **function mode**, using explicit function expressions.

---

# I. Constructor (`NumericalDerivative`)

The constructor stores all input fields and exposes them to the validator and executor.  
It does **not** perform validation or computation.

## 1. Stored Fields

- `function`: string expression in terms of `x` (and optionally `y`)
- `x`: evaluation point
- `y`: evaluation point for partial derivatives
- `h`: step size
- `calculation_mode`: selected derivative method
- `richardson_order`: optional integer for Richardson extrapolation

Example:

```python
{
    "function": "np.sin(x)",
    "x": 1.0,
    "h": 1e-4,
    "calculation_mode": "central"
}
```

The constructor does not modify or validate these values.

---

# II. Validator (`NumericalDerivativeValidator`)

The validator ensures that:

- Required fields exist  
- Types are correct  
- Step size is positive  
- Method‑specific constraints are satisfied  

---

## 1. Supported Modes

The validator checks:

```python
calculation_mode ∈ [
    "forward", "backward", "central",
    "richardson",
    "second_forward", "second_central",
    "third_forward",
    "partial_x", "partial_y"
]
```

---

## 2. Function

Must be a **non‑empty string**.

---

## 3. x and h

- `x` must be a real number  
- `h` must be a real number  
- `h > 0`  

---

## 4. Partial Derivatives

For:

- `partial_x`
- `partial_y`

the validator requires:

```python
y must be a real number
```

---

## 5. Richardson Order

For `richardson` mode:

- `richardson_order` must be a positive integer  
- Default: `2`

---

# III. Executor (`NumericalDerivativeExecutor`)

The executor performs the actual numerical differentiation.  
It dispatches based on `calculation_mode`:

```python
dispatch = {
    "forward": self.forward,
    "backward": self.backward,
    "central": self.central,
    ...
}
```

Each method returns a dictionary containing the derivative value.

---

# 1. Function Evaluation

The executor evaluates the function using:

```python
eval(expr, {"__builtins__": {}}, {"x": x, "y": y, "np": np})
```

This allows expressions like:

- `np.sin(x)`
- `x**2 + y**2`
- `np.exp(-x)`

---

# 2. First‑Order Derivatives

### Forward Difference

\[
f'(x) \approx \frac{f(x+h) - f(x)}{h}
\]

---

### Backward Difference

\[
f'(x) \approx \frac{f(x) - f(x-h)}{h}
\]

---

### Central Difference

\[
f'(x) \approx \frac{f(x+h) - f(x-h)}{2h}
\]

More accurate than forward/backward.

---

# 3. Richardson Extrapolation

Uses central differences at step sizes \( h \) and \( 2h \):

\[
D(h) = \frac{f(x+h) - f(x-h)}{2h}
\]

\[
D(2h) = \frac{f(x+2h) - f(x-2h)}{4h}
\]

Final estimate:

\[
D = D(h) + \frac{D(h) - D(2h)}{2^p - 1}
\]

where \( p \) is the Richardson order.

---

# 4. Higher‑Order Derivatives

### Second Forward

\[
f''(x) \approx \frac{f(x+2h) - 2f(x+h) + f(x)}{h^2}
\]

---

### Second Central

\[
f''(x) \approx \frac{f(x+h) - 2f(x) + f(x-h)}{h^2}
\]

---

### Third Forward

\[
f^{(3)}(x) \approx \frac{f(x+3h) - 3f(x+2h) + 3f(x+h) - f(x)}{h^3}
\]

---

# 5. Partial Derivatives

### Partial w.r.t. x

\[
\frac{\partial f}{\partial x}(x,y)
\approx \frac{f(x+h,y) - f(x-h,y)}{2h}
\]

---

### Partial w.r.t. y

\[
\frac{\partial f}{\partial y}(x,y)
\approx \frac{f(x,y+h) - f(x,y-h)}{2h}
\]

---

# IV. Example Calculation (Central Difference)

Compute:

\[
f(x) = \sin(x),\quad f'(1)
\]

Exact derivative:

\[
\cos(1) \approx 0.540302
\]

### Code Example

```python
from core.base_method import NumericalMethod

method = NumericalMethod(
    method="numerical_derivative",
    input_data={
        "function": "np.sin(x)",
        "x": 1.0,
        "h": 1e-4,
        "calculation_mode": "central"
    }
)

method.validate_input()
result = method.execute()
```

### Expected Output

```
derivative ≈ 0.540302
```

### Example Result Structure

```json
{
  "status": "success",
  "result": {
    "derivative": 0.540302,
    "calculation_mode": "central"
  }
}
```

---

# End of Document


---
