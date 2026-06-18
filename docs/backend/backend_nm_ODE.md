
---


```markdown
# NA‑Engine — ODE Module (Backend Documentation)

This document describes the backend implementation of the Ordinary Differential Equations (ODE) module in NA‑Engine.  
It covers the constructor, validator, executor, and example calculations for the supported methods.

Supported calculation modes:

- `euler`
- `heun`
- `rk2`
- `rk4`
- `rk4_system`
- `shooting`
- `finite_differences`
- `adams_bashforth_2`
- `adams_bashforth_3`
- `adams_moulton_2`

---

# I. Constructor (`ODE`)

The constructor only **stores** input data; it does not validate or compute.

## 1. Stored Fields

- `function`: string expression for \( f(x, y) \) (IVP, BVP)
- `system`: list of string expressions for systems \( \mathbf{y}' = \mathbf{f}(x, \mathbf{y}) \)
- `x0`: initial point
- `y0`: initial value (scalar or list for systems)
- `x_end`: final point
- `h`: step size
- `calculation_mode`: selected ODE method

### BVP‑specific fields

- `alpha`: boundary value at \( x_0 \)
- `beta`: boundary value at \( x_{\text{end}} \)
- `s0`: initial slope guess for shooting
- `n`: number of subintervals for finite differences

The constructor exposes these attributes to the validator and executor via `instance.input_data` and direct attributes.

---

# II. Validator (`ODEValidator`)

The validator enforces:

- Supported `calculation_mode`
- Presence and types of required fields
- Method‑specific constraints

## 1. Supported Modes

```python
SUPPORTED_MODES = [
    "euler", "heun", "rk2", "rk4",
    "rk4_system",
    "shooting",
    "finite_differences",
    "adams_bashforth_2",
    "adams_bashforth_3",
    "adams_moulton_2",
]
```

If `calculation_mode` is not in this list, a `ValidationError` is raised.

---

## 2. IVP Methods

For:

- `euler`
- `heun`
- `rk2`
- `rk4`
- `adams_bashforth_2`
- `adams_bashforth_3`
- `adams_moulton_2`

the validator requires:

- `function`: string
- `x0`, `y0`, `x_end`: real numbers
- `h`: positive real number

---

## 3. System of ODEs (`rk4_system`)

Requires:

- `system`: list of function strings
- `y0`: list (initial vector)

Each function in `system` is a string; `y0` length must match the system dimension (enforced implicitly in executor).

---

## 4. Shooting Method (BVP)

For `shooting`:

Required keys:

- `function`
- `x0`
- `x_end`
- `alpha`
- `beta`
- `s0`
- `h`

If any is missing, a `ValidationError` is raised.

---

## 5. Finite Differences (BVP)

For `finite_differences`:

- `n`: integer, `n >= 3`
- Required keys: `function`, `x0`, `x_end`, `alpha`, `beta`

---

# III. Executor (`ODEExecutor`)

The executor performs all ODE computations.  
It uses a dispatcher:

```python
dispatch = {
    "euler": self.euler,
    "heun": self.heun,
    "rk2": self.rk2,
    "rk4": self.rk4,
    "rk4_system": self.rk4_system,
    "shooting": self.shooting,
    "finite_differences": self.finite_differences,
    "adams_bashforth_2": self.adams_bashforth_2,
    "adams_bashforth_3": self.adams_bashforth_3,
    "adams_moulton_2": self.adams_moulton_2,
}
```

Each method returns a dictionary with the numerical solution.

---

## 1. Function Evaluation

All methods use a helper:

```python
_eval(expr, x, y)
```

which evaluates a string expression with:

- `x`, `y`
- `np` (NumPy)
- No built‑ins exposed

For systems, a local environment also includes `y1`, `y2`, … for each component.

---

## 2. Single‑Equation IVP Methods

### Euler

Explicit Euler:

\[
y_{n+1} = y_n + h f(x_n, y_n)
\]

Returns:

```json
{ "x": [...], "y": [...] }
```

---

### Heun (Improved Euler)

Two‑stage predictor–corrector:

\[
k_1 = f(x_n, y_n)
\]
\[
k_2 = f(x_n + h, y_n + h k_1)
\]
\[
y_{n+1} = y_n + \frac{h}{2}(k_1 + k_2)
\]

---

### RK2 (Midpoint)

\[
k_1 = f(x_n, y_n)
\]
\[
k_2 = f\left(x_n + \frac{h}{2}, y_n + \frac{h}{2}k_1\right)
\]
\[
y_{n+1} = y_n + h k_2
\]

---

### RK4

Classical 4th‑order Runge–Kutta:

\[
\begin{aligned}
k_1 &= f(x_n, y_n) \\
k_2 &= f(x_n + h/2, y_n + h k_1/2) \\
k_3 &= f(x_n + h/2, y_n + h k_2/2) \\
k_4 &= f(x_n + h, y_n + h k_3) \\
y_{n+1} &= y_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)
\end{aligned}
\]

---

## 3. RK4 for Systems (`rk4_system`)

For a system:

\[
\mathbf{y}' = \mathbf{f}(x, \mathbf{y})
\]

The executor:

- Stores `y` as a NumPy vector  
- Evaluates each component with access to `y`, `y1`, `y2`, …  
- Applies RK4 vector‑wise  

Returns:

```json
{ "x": [...], "y": [y_vec_0, y_vec_1, ...] }
```

where each `y_vec_i` is a NumPy array snapshot.

---

## 4. Shooting Method (BVP)

Solves a second‑order BVP:

\[
y'' = f(x, y),\quad y(x_0) = \alpha,\quad y(x_{\text{end}}) = \beta
\]

Steps:

1. Convert to system:
   \[
   y_1 = y,\quad y_2 = y'
   \]
2. Integrate IVP with RK4 for a given initial slope \( s = y'(x_0) \)
3. Use Newton iterations on \( s \) to match \( y(x_{\text{end}}) \approx \beta \)

The executor:

- Integrates twice: with `s` and `s + ε`
- Approximates derivative w.r.t. `s`
- Updates `s` using Newton’s method (fixed number of iterations)

Returns:

```json
{ "y_end": y(x_end; s*), "target": beta }
```

---

## 5. Finite Differences (BVP)

Solves:

\[
y'' = f(x, y),\quad y(x_0) = \alpha,\quad y(x_{\text{end}}) = \beta
\]

Discretization:

- Uniform grid with `n` subintervals
- Step size:
  \[
  h = \frac{x_{\text{end}} - x_0}{n}
  \]
- Interior nodes: \( i = 1, \dots, n-1 \)

Finite difference equation:

\[
y_{i-1} - 2y_i + y_{i+1} = h^2 f(x_i, y_i)
\]

The executor:

- Builds a tridiagonal matrix `A` of size `(n-1) × (n-1)`
- Builds RHS vector `b`, including boundary conditions via `alpha`, `beta`
- Solves `A y_inner = b`
- Concatenates `[alpha, y_inner, beta]`

Returns:

```json
{ "x": [...], "y": [...] }
```

---

## 6. Adams–Bashforth 2

Two‑step explicit multistep method:

\[
y_{n+1} = y_n + \frac{h}{2}\left(3 f_n - f_{n-1}\right)
\]

Startup:

- First step computed via RK2 (midpoint) to obtain \( y_1 \)

---

## 7. Adams–Bashforth 3

Three‑step explicit method:

\[
y_{n+1} = y_n + \frac{h}{12}\left(23 f_n - 16 f_{n-1} + 5 f_{n-2}\right)
\]

Startup:

- First two steps computed via RK4 to obtain \( y_1, y_2 \)

---

## 8. Adams–Moulton 2

Two‑step implicit method:

Predictor–corrector scheme:

1. Predictor (Adams–Bashforth 2):
   \[
   y_{\text{pred}} = y_n + \frac{h}{2}(3 f_n - f_{n-1})
   \]
2. Corrector (Adams–Moulton 2):
   \[
   y_{n+1} = y_n + \frac{h}{12}(5 f_{n+1} + 8 f_n - f_{n-1})
   \]
   solved by fixed‑point iterations on \( y_{n+1} \).

Returns:

```json
{ "x": [...], "y": [...] }
```

---

# IV. Example Calculation (RK4 IVP)

Solve:

\[
y' = y,\quad y(0) = 1,\quad x \in [0, 1]
\]

Exact solution:

\[
y(x) = e^x
\]

### Code Example

```python
from core.base_method import NumericalMethod

method = NumericalMethod(
    method="ode",
    input_data={
        "calculation_mode": "rk4",
        "function": "y",      # y' = y
        "x0": 0.0,
        "y0": 1.0,
        "x_end": 1.0,
        "h": 0.1
    }
)

method.validate_input()
result = method.execute()
```

### Example Result Structure

```json
{
  "status": "success",
  "result": {
    "x": [0.0, 0.1, 0.2, ... , 1.0],
    "y": [1.0, 1.10517, 1.22140, ...]
  }
}
```

---

# End of Document
```
