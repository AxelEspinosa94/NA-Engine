
---

# Finite Differences for BVPs — Theory

Finite differences approximate derivatives on a grid to solve boundary value problems.

---

## 1. Problem

$$
y'' = f(x, y), \quad y(x_0) = \alpha,\quad y(x_1) = \beta
$$

---

## 2. Grid

Divide \([x_0, x_1]\) into $n$ subintervals:

$$
x_i = x_0 + i h,\quad h = \frac{x_1 - x_0}{n},\quad i = 0,\dots,n
$$

Unknowns: $y_1, \dots, y_{n-1}$ (interior points).

---

## 3. Discretization

Central difference for second derivative:

$$
y''(x_i) \approx \frac{y_{i-1} - 2y_i + y_{i+1}}{h^2}
$$

Equation:

$$
\frac{y_{i-1} - 2y_i + y_{i+1}}{h^2} = f(x_i, y_i)
$$

This yields a nonlinear or linear system depending on $f$.

For linear problems, the system is typically tridiagonal.

---

## 4. Properties

- Directly enforces boundary conditions  
- Leads to algebraic systems solvable by linear algebra  
- Good for linear BVPs and moderate dimensions

---

# End of Document
```

---

### `theory_adams_bashforth.md`

```markdown
# Adams–Bashforth Methods — Theory

Adams–Bashforth methods are explicit multistep schemes for IVPs:

$$
y' = f(x, y)
$$

They use several past points to predict the next value.

---

## 1. AB2 (Two‑Step)

$$
y_{n+1} = y_n + \frac{h}{2}\left(3 f_n - f_{n-1}\right)
$$

where $f_n = f(x_n, y_n)$.

- Order: 2  
- Requires $y_0, y_1$ (startup via one‑step method like RK2/RK4)

---

## 2. AB3 (Three‑Step)

$$
y_{n+1} = y_n + \frac{h}{12}\left(23 f_n - 16 f_{n-1} + 5 f_{n-2}\right)
$$

- Order: 3  
- Requires $y_0, y_1, y_2$ (startup via RK4, for example)

---

## 3. Properties

- Efficient: reuse past evaluations  
- Explicit: no nonlinear solves per step  
- Stability more delicate than one‑step methods

---

# End of Document
```

---

### `theory_adams_moulton_2.md`

```markdown
# Adams–Moulton 2 (Trapezoidal Rule) — Theory

Adams–Moulton methods are implicit multistep schemes.  
The 2‑step version is closely related to the trapezoidal rule.

---

## 1. AM2 Formula

$$
y_{n+1} = y_n + \frac{h}{12}\left(5 f_{n+1} + 8 f_n - f_{n-1}\right)
$$

where $f_{n+1} = f(x_{n+1}, y_{n+1})$ depends on the unknown $y_{n+1}$.

---

## 2. Predictor–Corrector

To avoid solving a nonlinear equation exactly, a predictor–corrector scheme is used:

1. Predictor (e.g., AB2):

$$
y_{\text{pred}} = y_n + \frac{h}{2}(3 f_n - f_{n-1})
$$

2. Corrector (AM2):

$$
y_{n+1} \approx y_n + \frac{h}{12}\left(5 f(x_{n+1}, y_{\text{pred}}) + 8 f_n - f_{n-1}\right)
$$

Optionally iterate the corrector for more accuracy.

---

## 3. Properties

- Higher accuracy and better stability than explicit AB methods  
- Implicit nature improves behavior on stiff problems  
- Requires at least one predictor step

---

# End of Document

---
