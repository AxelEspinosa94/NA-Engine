
---

# NA‑Engine — Nonlinear Equation Solvers (Backend Documentation)

This document describes the backend implementation of the nonlinear equation solver module in NA‑Engine.  
It covers the constructor, validator, executor, and an example calculation for one of the supported methods.

Supported calculation modes:

- `fixed_point`
- `bisection`
- `newton`
- `secant`
- `false_position`

All nonlinear solvers operate exclusively in **function mode**.

---

# I. Constructor (`NonLinearEquation`)

The constructor is responsible for:

- Reading and validating basic input  
- Building symbolic and numeric versions of the function  
- Preparing method‑specific components (e.g., derivative, g(x), g'(x))  
- Storing tolerance, iteration limits, and initial values  

The nonlinear module **only supports**:

```
mode = "function"
```

## 1. Function

The user must provide:

```python
"function": "x**2 - 2"
```

The constructor:

- Parses the string using SymPy (`sympify`)
- Builds a NumPy‑compatible function using `lambdify`
- Stores the symbolic function for derivative computation

## 2. Method‑specific components

### Fixed Point
Requires:

- `g(x)` as a string
- `g'(x)` is computed symbolically

### Newton
Requires:

- `f'(x)` computed symbolically

### Secant
Requires:

- Two initial guesses: `x0` and `x1`

### Bisection / False Position
Require:

- An interval `[a, b]`

## 3. Tolerance and Iterations

The constructor validates:

- `tol` must be a positive number  
- `max_iter` must be a positive integer  

## 4. Initial Values

Depending on the method:

- `x0` for Newton and Fixed Point  
- `x0` and `x1` for Secant  
- `interval` for Bisection and False Position  

---

# II. Validator (`NonLinearValidator`)

The validator performs all method‑specific checks before the constructor runs.

## 1. Supported Methods

The validator ensures:

```python
calculation_mode ∈ {
    "fixed_point",
    "bisection",
    "newton",
    "secant",
    "false_position"
}
```

## 2. Mode

Nonlinear solvers only support:

```
mode = "function"
```

## 3. Function

Must be a valid string expression.

## 4. Method‑specific validations

### Fixed Point
- Requires `g(x)`  
- Requires `x0`

### Bisection
- Requires interval `[a, b]`

### False Position
- Requires interval `[a, b]`

### Newton
- Requires `x0`

### Secant
- Requires `x0` and `x1`

If any rule fails, a `ValidationError` is raised.

---

# III. Executor (`NonLinearExecutor`)

The executor dispatches to one of the following algorithms:

- Fixed Point Iteration  
- Bisection  
- Newton’s Method  
- Secant Method  
- False Position (Regula Falsi)  

It returns a dictionary containing:

- `"root"`: the approximated solution  
- `"iterations"`: number of iterations performed  
- `"calculation_mode"`  
- `"tol"`  

---

## 1. Fixed Point Iteration

Uses:

\[
x_{k+1} = g(x_k)
\]

Before iteration begins, the executor checks:

\[
|g'(x_0)| < 1
\]

If not, the method may diverge.

Stopping criterion:

\[
|x_{k+1} - x_k| < \text{tol}
\]

---

## 2. Bisection Method

Requires a sign change:

\[
f(a)f(b) < 0
\]

Iteration:

\[
c = \frac{a + b}{2}
\]

Stopping criteria:

- \(|f(c)| < \text{tol}\)  
- \(|b - a| < \text{tol}\)

---

## 3. Newton’s Method

Uses:

\[
x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}
\]

The executor checks:

- Derivative is finite  
- Derivative is not zero  
- Next iterate is finite  

Stopping criterion:

\[
|x_{k+1} - x_k| < \text{tol}
\]

---

## 4. Secant Method

Uses:

\[
x_{k+1} = x_k - f(x_k)\frac{x_k - x_{k-1}}{f(x_k) - f(x_{k-1})}
\]

The executor checks:

- Denominator is not zero  
- Next iterate is finite  

Stopping criterion:

\[
|x_{k+1} - x_k| < \text{tol}
\]

---

## 5. False Position (Regula Falsi)

Requires a sign change:

\[
f(a)f(b) < 0
\]

Iteration:

\[
c = b - f(b)\frac{b - a}{f(b) - f(a)}
\]

Stopping criterion:

\[
|f(c)| < \text{tol}
\]

---

# IV. Example Calculation (Newton’s Method)

Below is a complete example using **Newton’s method** to solve:

\[
f(x) = x^2 - 2
\]

The exact root is:

\[
\sqrt{2} \approx 1.41421356
\]

### Code Example

```python
from core.base_method import NumericalMethod

method = NumericalMethod(
    method="nonlinear",
    input_data={
        "mode": "function",
        "calculation_mode": "newton",
        "function": "x**2 - 2",
        "x0": 1.0,
        "tol": 1e-6,
        "max_iter": 50
    }
)

method.validate_input()
result = method.execute()
```

### Expected Output

Newton’s method converges rapidly:

```
root ≈ 1.41421356
```

### Example Result Structure

```json
{
  "status": "success",
  "result": {
    "root": 1.41421356,
    "iterations": 5,
    "calculation_mode": "newton",
    "tol": 1e-6
  }
}
```

---

# End of Document

---

