
---

# NA‑Engine — Numerical Integration Module (Backend Documentation)

This document describes the backend implementation of the unified integration module in NA‑Engine.  
It covers the constructor, validator, executor, and an example calculation for each supported integration method.

Supported calculation modes:

- `trapezoid_simple`
- `trapezoid_composite`
- `simpson_1_3`
- `simpson_3_8`
- `romberg`
- `gauss` (Gauss–Legendre)

All integration methods operate exclusively in **function mode**.

---

# I. Constructor (`Integral`)

The constructor is responsible for:

- Reading and validating basic input  
- Building the function to integrate  
- Creating the evaluation grid for composite rules  
- Preparing symbolic and numeric structures  

The integration module **only supports**:

```
mode = "function"
```

## 1. Function

The user must provide:

```python
"function": "sin(x) + x**2"
```

The constructor:

- Parses the string using SymPy (`sympify`)
- Builds a NumPy‑compatible function using `lambdify`

## 2. Interval

The interval must be:

```
"interval": [a, b]
```

with `a < b`.

## 3. n (subintervals or Romberg depth)

The parameter `n` is interpreted differently depending on the method:

- Composite rules → number of subintervals  
- Romberg → depth of the Romberg table  
- Gauss → ignored (Gauss uses `gauss_points` instead)

The constructor ensures:

- `n` is a positive integer  
- The grid `x` is built as:

\[
x_i = a + i\frac{b-a}{n},\quad i = 0,\dots,n
\]

and:

\[
y_i = f(x_i)
\]

---

# II. Validator (`IntegrationValidator`)

The validator performs all method‑specific checks before the constructor runs.

## 1. Supported Modes

The validator ensures:

```python
calculation_mode ∈ {
    "trapezoid_simple",
    "trapezoid_composite",
    "simpson_1_3",
    "simpson_3_8",
    "romberg",
    "gauss"
}
```

## 2. Mode

Integration only supports:

```
mode = "function"
```

Any other mode raises a `ValidationError`.

## 3. Function

Must be a valid string expression.

## 4. Interval

Must be a list or tuple `[a, b]` with `a < b`.

## 5. n (subintervals or depth)

Must be:

- Integer  
- Positive  

## 6. Method‑specific constraints

The validator enforces:

| Method | Constraint |
|--------|------------|
| trapezoid_simple | `n == 1` |
| trapezoid_composite | `n >= 1` |
| simpson_1_3 | `n` even |
| simpson_3_8 | `n` multiple of 3 |
| romberg | no constraint |
| gauss | no constraint |

## 7. Gauss‑Legendre specific

If `gauss_points > 50`, a `ValidationError` is raised due to numerical instability.

---

# III. Executor (`IntegrationExecutor`)

The executor dispatches to one of the following algorithms:

- Composite rules  
- Romberg integration  
- Gauss–Legendre quadrature  

It returns a dictionary containing:

- `"value"`: numerical approximation  
- `"calculation_mode"`  
- `"a"` and `"b"`  
- `"n"` or `"gauss_points"`  

---

## 1. Composite Rules

Composite rules use the grid built by the constructor:

\[
x_0, x_1, \dots, x_n
\]

with:

\[
h = \frac{b - a}{n}
\]

### 1.1 Trapezoid (simple)

\[
T = \frac{h}{2}(f(x_0) + f(x_n))
\]

### 1.2 Trapezoid (composite)

\[
T = h\left[\frac{f(x_0)}{2} + \sum_{i=1}^{n-1} f(x_i) + \frac{f(x_n)}{2}\right]
\]

### 1.3 Simpson 1/3

Requires even `n`.

\[
S = \frac{h}{3}\left[f(x_0) + f(x_n) + 4\sum_{\text{odd}} f(x_i) + 2\sum_{\text{even}} f(x_i)\right]
\]

### 1.4 Simpson 3/8

Requires `n` multiple of 3.

\[
S = \frac{3h}{8}\left[f(x_0) + f(x_n) + 3\sum_{i\not\equiv 0\ (3)} f(x_i) + 2\sum_{i\equiv 0\ (3)} f(x_i)\right]
\]

---

## 2. Romberg Integration

Romberg builds a triangular table:

\[
R_{k,0} = T(h_k)
\]

\[
R_{k,j} = R_{k,j-1} + \frac{R_{k,j-1} - R_{k-1,j-1}}{4^j - 1}
\]

The final value is:

\[
R_{n,n}
\]

---

## 3. Gauss–Legendre Quadrature

The method computes:

- Legendre polynomial roots \( t_i \)
- Weights \( w_i \)
- Transforms them to \([a, b]\)

\[
x_i = \frac{b-a}{2}t_i + \frac{a+b}{2}
\]

\[
\int_a^b f(x)\,dx \approx \frac{b-a}{2}\sum_{i=1}^{n} w_i f(x_i)
\]

---

# IV. Example Calculation

Below is a complete example using **Simpson 1/3**.

```python
from core.base_method import NumericalMethod

method = NumericalMethod(
    method="integration",
    input_data={
        "mode": "function",
        "calculation_mode": "simpson_1_3",
        "function": "x**2",
        "interval": [0, 2],
        "n": 4
    }
)

method.validate_input()
result = method.execute()
```

### Expected Output

The exact integral is:

\[
\int_0^2 x^2\,dx = \frac{8}{3} \approx 2.6666667
\]

Simpson 1/3 with \( n = 4 \) yields:

```
value ≈ 2.6666667
```

### Example Result Structure

```json
{
  "status": "success",
  "result": {
    "value": 2.6666667,
    "calculation_mode": "simpson_1_3",
    "a": 0.0,
    "b": 2.0,
    "n": 4
  }
}
```

---

# End of Document

---

