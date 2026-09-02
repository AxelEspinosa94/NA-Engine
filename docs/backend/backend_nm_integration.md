
---

# **NA‑Engine — Numerical Integration Module (Backend Documentation)**

## **Table of Contents**
- [1. Overview](#1-overview)
- [2. Constructor — `Integral`](#2-constructor--integral)
- [3. Validator — `IntegrationValidator`](#3-validator--integrationvalidator)
- [4. Executor — `IntegrationExecutor`](#4-executor--integrationexecutor)
- [5. Supported Methods](#5-supported-methods)
- [6. Method Algorithms](#6-method-algorithms)
- [7. Example Calculation](#7-example-calculation)
- [8. Extension Guide](#8-extension-guide)

---

# **1. Overview**

The Integration Module in NA‑Engine provides a unified backend for multiple numerical integration techniques.  
It follows the same architectural philosophy as all NA‑Engine modules:

- **Constructor Layer** → parses and structures input  
- **Validator Layer** → ensures mathematical validity  
- **Executor Layer** → performs the numerical computation  
- **Catalog JSON** → declares supported modes and rule scripts  
- **Modular folder structure** → scalable and consistent across modules  

Supported calculation modes:

- `trapezoid_simple`
- `trapezoid_composite`
- `simpson_1_3`
- `simpson_3_8`
- `romberg`
- `gauss` (Gauss–Legendre)
- `clenshaw_curtis`

All integration methods operate exclusively in:

```
mode = "function"
```

---

# **2. Constructor — `Integral`**

The constructor prepares all data required for numerical integration.

### **Responsibilities**

- Parse the function expression  
- Build a NumPy‑compatible function  
- Validate basic structural input  
- Build evaluation grids (for composite rules)  
- Store interval and parameters (`n`, `gauss_points`)  

### **2.1 Function Parsing**

Input:

```python
"function": "sin(x) + x**2"
```

The constructor:

- Parses the string using SymPy (`sympify`)
- Converts it to a NumPy function via `lambdify`

### **2.2 Interval**

Must be:

```
"interval": [a, b]
```

with `a < b`.

### **2.3 Parameter `n`**

Interpreted differently depending on the method:

| Method | Meaning of `n` |
|--------|----------------|
| Composite rules | Number of subintervals |
| Simpson rules | Number of subintervals (with constraints) |
| Romberg | Depth of Romberg table |
| Gauss | Ignored (uses `gauss_points`) |
| Clenshaw–Curtis | Number of Chebyshev subintervals (must be even) |

The constructor builds the grid:

$$
x_i = a + i\frac{b-a}{n},\quad i = 0,\dots,n
$$

and evaluates:

$$
y_i = f(x_i)
$$

---

# **3. Validator — `IntegrationValidator`**

The validator ensures mathematical correctness of the input.

### **3.1 Supported Modes**

The validator checks that:

```python
calculation_mode ∈ SUPPORTED_MODES
```

Declared in:

```
strategies/validators/integration/integration_validation_catalog.json
```

### **3.2 Mode**

Integration only supports:

```
mode = "function"
```

### **3.3 Function**

Must be a valid SymPy expression.

### **3.4 Interval**

Must be `[a, b]` with `a < b`.

### **3.5 Parameter `n`**

Must be:

- integer  
- positive  

### **3.6 Method‑specific constraints**

| Method | Constraint |
|--------|------------|
| trapezoid_simple | `n == 1` |
| trapezoid_composite | `n >= 1` |
| simpson_1_3 | `n % 2 == 0` |
| simpson_3_8 | `n % 3 == 0` |
| romberg | no constraint |
| gauss | no constraint |
| clenshaw_curtis | `n % 2 == 0` |

### **3.7 Gauss‑Legendre**

If:

```
gauss_points > 50
```

raise `ValidationError` (numerical instability).

---

# **4. Executor — `IntegrationExecutor`**

The executor performs the numerical computation.  
It dispatches based on `instance.calculation_mode`:

- Composite rules  
- Simpson rules  
- Romberg  
- Gauss–Legendre  
- Clenshaw–Curtis  

### **Return Structure**

```python
{
    "value": float,
    "calculation_mode": str,
    "a": float,
    "b": float,
    "n": int,
    "gauss_points": int (optional)
}
```

---

# **5. Supported Methods**

### **5.1 Composite Rules**
- Trapezoid (simple)
- Trapezoid (composite)
- Simpson 1/3
- Simpson 3/8

### **5.2 Romberg Integration**

Recursive Richardson extrapolation.

### **5.3 Gauss–Legendre Quadrature**

Uses Legendre roots and weights.

### **5.4 Clenshaw–Curtis Quadrature**

Uses Chebyshev nodes + DCT‑I + cosine expansion.

---

# **6. Method Algorithms**

## **6.1 Composite Rules**

Grid:

$$
x_0, x_1, \dots, x_n
$$

Step:

$$
h = \frac{b-a}{n}
$$

### **Trapezoid (simple)**

$$
T = \frac{h}{2}(f(x_0) + f(x_n))
$$

### **Trapezoid (composite)**

$$
T = h\left[\frac{f(x_0)}{2} + \sum_{i=1}^{n-1} f(x_i) + \frac{f(x_n)}{2}\right]
$$

### **Simpson 1/3**

$$
S = \frac{h}{3}\left[f(x_0) + f(x_n) + 4\sum_{\text{odd}} f(x_i) + 2\sum_{\text{even}} f(x_i)\right]
$$

### **Simpson 3/8**

$$
S = \frac{3h}{8}\left[f(x_0) + f(x_n) + 3\sum_{i\not\equiv 0\ (3)} f(x_i) + 2\sum_{i\equiv 0\ (3)} f(x_i)\right]
$$

---

## **6.2 Romberg Integration**

$$
R_{k,0} = T(h_k)
$$

$$
R_{k,j} = R_{k,j-1} + \frac{R_{k,j-1} - R_{k-1,j-1}}{4^j - 1}
$$

Final value:

$$
R_{n,n}
$$

---

## **6.3 Gauss–Legendre Quadrature**

Roots:

$$
t_i
$$

Weights:

$$
w_i
$$

Mapping:

$$
x_i = \frac{b-a}{2}t_i + \frac{a+b}{2}
$$

Integral:

$$
\int_a^b f(x)\,dx \approx \frac{b-a}{2}\sum w_i f(x_i)
$$

---

## **6.4 Clenshaw–Curtis Quadrature**

Chebyshev nodes:

$$
t_n = \cos\left(\frac{n\pi}{N}\right)
$$

Mapping:

$$
x_n = \frac{b-a}{2}t_n + \frac{a+b}{2}
$$

DCT‑I:

$$
a_k = \frac{2}{N}\left[\frac{f_0}{2} + \frac{f_N}{2}(-1)^k + \sum f_n\cos\left(\frac{nk\pi}{N}\right)\right]
$$

Integral:

$$
I = a_0 + \sum_{m=1}^{N/2} \frac{2a_{2m}}{1-(2m)^2}
$$

Scale:

$$
\int_a^b f(x)\,dx = \frac{b-a}{2}I
$$

---

# **7. Example Calculation**

Using **Simpson 1/3**:

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

Exact integral:

$$
\int_0^2 x^2\,dx = \frac{8}{3}
$$

Output:

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

# **8. Extension Guide**

## **8.1 Adding a New Method — `<new-method>`**

1. Add validation rules in:

```
strategies/validators/integration/integration_validation_catalog.json
```

2. Add `_run_<new-method>()` to `IntegrationExecutor`.

3. Add constraints to `_validate_n_for_mode()` if needed.

4. Register the method in:

```
method_catalog.json
```

Example:

```json
"<new-method>": {
  "classExecutor": "strategies.executors.integration_executors.IntegrationExecutor",
  "classInputValidator": "strategies.validators.integration.IntegrationValidator",
  "classConstructor": "strategies.constructors.integration.Integral"
}
```

5. Add documentation.

---

## **8.2 Adding a New Module — `<new-module>`**

Follow the NA‑Engine architecture:

```
strategies/
  constructors/<new-module>/
  validators/<new-module>/
  executors/<new-module>/
```

Add:

- `<new-module>_validation_catalog.json`
- `<new-module>_validators.py`
- `<new-module>_executors.py`
- `<new-module>_constructor.py`

Register in `method_catalog.json`.

---

# **End of Document**

---
